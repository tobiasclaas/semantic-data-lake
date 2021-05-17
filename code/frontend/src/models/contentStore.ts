import CommonStore from "./commonStore"

abstract class ContentStore extends CommonStore {
    constructor() {
        super()
    }
    
    abstract getView(): React.ReactElement
}

export default ContentStore