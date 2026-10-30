import QtQml
QtObject {
    readonly property bool mock: true
    enum SortMode { SortLastActivated }
    enum GroupMode { GroupDisabled }
    property int sortMode
    property int groupMode
    property var rows: []
    readonly property int count: rows.length
    property var activeTask: ({row: -1, valid: false})
    property var calls: []
    function makeModelIndex(i) { return {row: i, valid: i >= 0 && i < rows.length}; }
    function makePersistentModelIndex(i) { return makeModelIndex(i); }
    function data(idx, role) {
        const row = rows[idx.row];
        if (!row) return role === 2 ? false : [];
        if (role === 0) return row.activities;
        if (role === 1) return row.desktops;
        return row.hidden;
    }
    function requestToggleMinimized(idx) {
        calls = calls.concat([idx.row]);
        rows[idx.row].hidden = !rows[idx.row].hidden;
        rowsChanged();
    }
}
