import { action, makeObservable, observable } from 'mobx'
import React from 'react'
import ContentStore from '../../../models/contentStore'
import appStore from '../../../stores/app.store'
import View from './main.component'

class ViewModel extends ContentStore {
    constructor() {
        super()
        makeObservable(this)
    }

    getView = () => <View viewModel={this} />
}


export default ViewModel