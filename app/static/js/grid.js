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
jQuery(document).ready(function(){

    grid = jQuery("#keynav").jqGrid({
        url:'/list/',
        ajaxGridOptions: { contentType: 'application/json; charset=utf-8' },
        datatype: "json",
        loadonce: true,
        colNames:['#', 'Наименование', 'Авторы','Дата', 'id', 'body'],
        colModel:[
            {name:'count',index:'count', width:20, align:"right"},
            {name:'name', index:'name', width:200},
            {name:'authors',index:'authors', width:100},
            {name:'date',index:'date', width:60, align:"right", formatter:'date', formatoptions: {srcformat:'Y-m-d h:i:s.000000', newformat:'d.m.Y h:i'}},
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
        //rowList:['1000000000'],
        //pager: '#pkeynav',
        sortname: 'date',
        viewrecords: true,
        sortorder: "desc",
        /* multiselect: true,*/
        caption: "List",
        height: '400',
        width: '800',
        /* beforeSelectRow: handleMultiSelect */
        onSelectRow: function(id){ 
            var row = $(this).jqGrid('getRowData', id);
            $('#body').html(row.body); 
        } 
    }).jqGrid('hideCol', 'cb');

    grid.jqGrid('navGrid',/*'#pkeynav'*/'',{edit:false,add:false,del:false});
    grid.jqGrid('bindKeys', {"onEnter":function( rowid ) { alert("You enter a row with id:"+rowid)} } );
    grid.jqGrid('navGrid',/*'#pkeynav'*/'',{edit:false,add:false,del:false});

    $.ctrl = function(key, callback, args) {
        var isCtrl = false;
        $(grid).keydown(function(e) {
            if(!args) args=[]; // IE barks when args is null

            if(e.ctrlKey) isCtrl = true;
            if(e.keyCode == key.charCodeAt(0) && isCtrl) {
                callback.apply(this, args);
                return false;
            }
        }).keyup(function(e) {
            if(e.ctrlKey) isCtrl = false;
        });
    };




/*
    $.ctrl('A', function() {
        grid.jqGrid('resetSelection');
        var ids = grid.getDataIDs();
        for (var i=0, il=ids.length; i < il; i++) {
            grid.jqGrid('setSelection',ids[i], true);
        }
    });
*/




});

