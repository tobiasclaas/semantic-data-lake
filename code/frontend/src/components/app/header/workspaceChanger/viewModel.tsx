import { action, computed, makeObservable, observable } from 'mobx'
import { IWorkspace, IWorkspaceExchange } from '../../../../models/workspace'
import workspacesStore from '../../../../stores/workspaces.store'

class ViewModel {
    @observable isDialogOpen: boolean = false
    @observable workspaceName: string = ''
    @observable anchorEl: null | HTMLElement = null

    @computed get isMenuOpen() {
        return Boolean(this.anchorEl)
    }

    constructor() {
        makeObservable(this)
    }

    @action openDialog() {
        this.closeMenu()
        this.isDialogOpen = true
        this.workspaceName = ''
    }

    @action closeDialog() {
        this.isDialogOpen = false
    }

    @action setWorkspaceName(newValue: string) {
        this.workspaceName = newValue
    }

    @action setAnchorEl(newValue: HTMLElement) {
        this.anchorEl = newValue
    }

    @action closeMenu() {
        this.anchorEl = null
    }

    changeWorkspace(item: IWorkspace) {
        workspacesStore.setCurrentWorkspace(item)
        this.closeMenu()
    }

    addNewWorkspace() {
        workspacesStore.addWorkspace({
            name: this.workspaceName
        } as IWorkspaceExchange)
        this.closeDialog()
    }
}

export default ViewModel