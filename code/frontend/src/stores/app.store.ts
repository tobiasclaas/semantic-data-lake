import { observable, action, makeObservable, computed } from "mobx"
import StoreStatus from "../models/storeStatus.enum"
import ContentStore from "../models/contentStore"

class AppStore {
    @observable status: StoreStatus = StoreStatus.uninitialized
    @observable errorMessage: string = ''


    // content manipulation
    @observable contentViewModel: ContentStore | null = null
    @computed get view() {
        if (!this.contentViewModel)
            return null
        return this.contentViewModel.getView()
    }
    
    @computed get isFullscreen() {
        if (!this.contentViewModel)
            return false
        return this.contentViewModel.isFullscreen
    }

    @action setContentViewModel(newValue: ContentStore | null) {
        this.contentViewModel = newValue
    }
    // end: content manipulation

    constructor() {
        makeObservable(this)
    }


    @action setStatus(newValue: StoreStatus) {
        this.status = newValue
    }

    @action setErrorMessage(newValue: string) {
        this.errorMessage = newValue
    }
}

const appStore = new AppStore()
export default appStore