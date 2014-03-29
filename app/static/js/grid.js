var handleMultiSelect = function (rowid, e) {
    var grid = $(this);
    if (!e.ctrlKey && !e.shiftKey) {
        grid.jqGrid('resetSelection');
    }
    else if (e.shiftKey) {
        var initialRowSelect = grid.jqGrid('getGridParam', 'selrow');

        grid.jqGrid('resetSelection');

        var CurrentSelectIndex = grid.jqGrid('getInd', rowid);
        var InitialSelectIndex = grid.jqGrid('getInd', initialRowSelect);
        var startID = "";
        var endID = "";
        if (CurrentSelectIndex > InitialSelectIndex) {
            startID = initialRowSelect;
            endID = rowid;
        }
        else {
            startID = rowid;
            endID = initialRowSelect;
        }
        var shouldSelectRow = false;
        $.each(grid.getDataIDs(), function (_, id) {
            if ((shouldSelectRow = id == startID || shouldSelectRow)) {
                grid.jqGrid('setSelection', id, false);
            }
            return id != endID;
        });
    }
    return true;
};
function makeLink(cellValue, options, rowdata, action) 
{
    return "<a target='_new' href='http://flibusta.net/b/" + cellValue + "' >"+cellValue+"</a>";
}   

var grid = {}
var stack = [];
jQuery(document).ready(function(){
    grid = jQuery("#grid").jqGrid({
        url:'/list/',
        ajaxGridOptions: { contentType: 'application/json; charset=utf-8' },
        datatype: "json",
        loadonce: true,
        colNames:['#', 'Наименование', 'Авторы','Дата', 'id', 'body'],
        colModel:[
            {name:'count',index:'count', width:20, align:"right"},
            {name:'name', index:'name', width:200},
            {name:'authors',index:'authors', width:100},
            {name:'dt',index:'date', width:60, align:"right", formatter:'date', formatoptions: {srcformat:'Y-m-d h:i:s.000000', newformat:'d.m.Y h:i'}},
            {name:'id',index:'id', width:50, formatter: makeLink, align: "center"},
            {name: 'body', index: '', hidden: true }

        ],
        jsonReader: {
            repeatitems : false,
            loadonce: true,
            root: function (obj) { return obj.rows; },
            page: function (obj) { return grid.jqGrid('getGridParam', 'page'); },
            total: function (obj) { return Math.ceil(obj.rows.length / grid.jqGrid('getGridParam', 'rowNum')); },
            records: function (obj) { return obj.rows.length; }
        },
        rowNum:-1,
        autwidth: true,
        sortname: 'date',
        viewrecords: true,
        sortorder: "desc",
        caption: "List",
        height: '400',
        width: '800',
        /* multiselect: true,*/
        /* beforeSelectRow: handleMultiSelect */
        onSelectRow: function(id){ 
            var row = $(this).jqGrid('getRowData', id);
            $('#body').html(row.body); 
        } 
    }).jqGrid('hideCol', 'cb');

    grid.jqGrid('navGrid',/*'#pkeynav'*/'',{edit:false,add:false,del:false});

    //grid.jqGrid('bindKeys', {"onEnter":function( rowid ) { alert("You enter a row with id:"+rowid)} } );

    function next(selectedRow){
        var ids = grid.getDataIDs();
        var index = grid.getInd(selectedRow);
        if (ids.length < 2) return;
        index++;
        if (index > ids.length)
            index = 1;
        grid.setSelection(ids[index - 1], true);
    }

    $(grid).keydown(function(e) {
        var row = grid.jqGrid('getGridParam','selrow');
        switch(e.keyCode){
            case 45: //Ins
            case 82: //r
                $.ajax({
                   type: "GET",
                   url: "/read/post/"+row,
                    success: function(msg){
                        stack.push("/unread/post/"+row);
                        $.growlUI(msg.result);
                        next(row);
                        grid.delRowData(row);
                        $("#grid").focus();
                   }
                 });
                $("#grid").focus();
                break;

            case 66://b
                $.ajax({
                   type: "GET",
                   url: "/read/book/"+row,
                   success: function(msg){
                       stack.push("/unread/book/"+row);
                       $.growlUI(msg.result);
                       next(row);
                       grid.delRowData(row);
                       $("#grid").focus();
                   }
                 });
                break;

            case 65://a
                $.ajax({
                   type: "GET",
                   url: "/read/author/"+row,
                   success: function(msg){
                       stack.push("/unread/author/"+row);
                       $.growlUI(msg.result);
                       grid.delRowData(row);
                       next(row);
                       $("#grid").focus();
                   }
                 });
                break;

            case 85: //u
                if(stack.length == 0)
                    return;
                var url = stack.pop()
                $.ajax({
                   type: "GET",
                   url: url,
                   success: function(msg){
                       newGrid = $("#grid").jqGrid('setGridParam',{url:"/list/", datatype:"json"}).trigger("reloadGrid");
                       $.growlUI("", msg.result, 2, function(){grid.setSelection(url.split("/").pop())});
//                       newGrid = grid.setSelection(url.split("/").pop());
                   }
                });
                $("#grid").focus();
                break;
        }
    });
});

