import { observable, action, makeObservable, computed, toJS } from "mobx"
import StoreStatus from "../models/storeStatus.enum"
import workspacesStore from "./workspaces.store"

export enum DisplayMode {
    primary = 0,
    workspaces = 1
}


class SettingsDialogStore {
    // other control props
    @observable isOpen: boolean = false
    @observable displayMode: DisplayMode = DisplayMode.workspaces
    @observable status: StoreStatus = StoreStatus.ready

    constructor() {
        makeObservable(this)
    }

    @action open() {
        if (workspacesStore.workspaces.length == 0) return
        this.displayMode = DisplayMode.primary
        this.isOpen = true
        this.status = StoreStatus.ready
    }

    @action close() {
        this.isOpen = false
    }

    @action setDisplayMode(newValue: DisplayMode) {
        // nothing to change
        if (this.displayMode === newValue) return

        this.displayMode = newValue
    }

    @action setStatus(newValue: StoreStatus) {
        this.status = newValue
    }
}

const settingsDialogStore = new SettingsDialogStore()
export default settingsDialogStore
