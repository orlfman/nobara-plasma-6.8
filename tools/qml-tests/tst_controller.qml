import QtQuick
import QtTest
import "../../usr/share/plasma/plasmoids/org.kde.plasma.nobara.showdesktop/contents/ui" as Nobara
TestCase {
    name: "NobaraMinimizeController"
    function i18nc(context, text) { return text; }
    Component { id: factory; Nobara.MinimizeAllController {} }
    property var controller
    function init() {
        controller = factory.createObject(this);
        verify(controller !== null);
        // Never invoke window operations unless the task model is our test double.
        verify(controller.tasksModel.mock === true);
    }
    function cleanup() { controller.destroy(); }
    function row(activities, desktops, hidden) {
        return {activities: activities, desktops: desktops, hidden: hidden};
    }
    function test_filter_and_restore() {
        const tasks = controller.tasksModel;
        tasks.rows = [row(["workA"], [1], false), row([], [], false),
                      row(["other"], [1], false), row(["workA"], [2], false),
                      row(["workA"], [1], true)];
        controller.toggle();
        compare(tasks.calls, [1, 0]);
        compare(controller.active, true);
        controller.toggle();
        compare(tasks.calls, [1, 0, 1, 0]);
        compare(controller.active, false);
        compare(tasks.rows[4].hidden, true);
    }
    function test_restored_and_closed_windows_are_skipped() {
        const tasks = controller.tasksModel;
        tasks.rows = [row([], [], false), row([], [], false), row([], [], false)];
        controller.toggle();
        tasks.rows[1].hidden = false;
        controller.minimizedClients[controller.activityDesktopId][0].valid = false;
        tasks.calls = [];
        controller.toggle();
        compare(tasks.calls, [0]);
    }
    function test_focus_change_clears_restore_state() {
        const tasks = controller.tasksModel;
        tasks.rows = [row(["workA"], [1], false)];
        controller.toggle();
        compare(controller.active, true);
        tasks.activeTask = tasks.makeModelIndex(0);
        compare(controller.active, false);
        compare(controller.minimizedClients[controller.activityDesktopId].length, 0);
    }
    function test_empty_and_other_desktop_state() {
        controller.toggle();
        compare(controller.active, true);
        controller.toggle();
        compare(controller.active, false);
        controller.tasksModel.rows = [row(["workA"], [1], false)];
        controller.toggle();
        controller.virtualDesktopInfo.currentDesktop = 2;
        compare(controller.active, false);
        controller.virtualDesktopInfo.currentDesktop = 1;
        compare(controller.active, true);
        controller.toggle();
        compare(controller.active, false);
    }
}
