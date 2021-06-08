import { action, observable } from "mobx"
import CommonStore from "./commonStore"

abstract class ContentStore extends CommonStore {
    constructor() {
        super()
    }

    @observable isFullscreen: boolean = false
    @action setFullscreen(isFullscreen: boolean) {
        this.isFullscreen = isFullscreen
    }
    
    abstract getView(): React.ReactElement
}

export default ContentStore