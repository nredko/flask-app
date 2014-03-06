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

var grid = {}
jQuery(document).ready(function(){

    grid = jQuery("#keynav").jqGrid({
        url:'/list/',
        ajaxGridOptions: { contentType: 'application/json; charset=utf-8' },
        datatype: "json",
        loadonce: true,
        colNames:['count', 'name', 'authors','date', 'id', 'body'],
        colModel:[
            {name:'count',index:'count', width:90, align:"right"},
            {name:'name', index:'name', width:100},
            {name:'authors',index:'authors', width:80},
            {name:'date',index:'date', width:80, align:"right"},
            {name:'id',index:'id', width:80},
            {name: 'body', index: '', hidden: true }

        ],
        jsonmap:[
            {name:'count',index:'count', width:90, align:"right"},
            {name:'name', index:'name', width:100},
            {name:'authors',index:'authors', width:80},
            {name:'date',index:'date', width:80, align:"right"},
            {name:'id',index:'id', width:80},
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
        width:1000,
        //rowList:['1000000000'],
        //pager: '#pkeynav',
        sortname: 'date',
        viewrecords: true,
        sortorder: "desc",
        multiselect: true,
        caption: "Keyboard Navigation",
        height: '600',
        autowidth: true,
        beforeSelectRow: handleMultiSelect
    }).jqGrid('hideCol', 'cb');

    jQuery("#keynav").jqGrid('navGrid',/*'#pkeynav'*/'',{edit:false,add:false,del:false});
    jQuery("#keynav").jqGrid('bindKeys', {"onEnter":function( rowid ) { alert("You enter a row with id:"+rowid)} } );

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

    $.ctrl('A', function() {
        grid.jqGrid('resetSelection');
        var ids = grid.getDataIDs();
        for (var i=0, il=ids.length; i < il; i++) {
            grid.jqGrid('setSelection',ids[i], true);
        }
    });
});

