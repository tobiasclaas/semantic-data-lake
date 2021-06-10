import { runInAction } from 'mobx'
import { action, makeObservable, observable } from 'mobx'
import React from 'react'
import ContentStore from '../../../models/contentStore'
import appStore from '../../../stores/app.store'
import View from './main.component'

class ViewModel extends ContentStore {
    constructor() {
        super()
        this.isFullscreen = true
        makeObservable(this)
    }

    getView = () => <View viewModel={this} />

    onDragStart = (event: React.DragEvent<HTMLElement>, nodeType: string) => {
        event.dataTransfer.setData('application/reactflow', nodeType);
        event.dataTransfer.effectAllowed = 'move';
    };
}


export default ViewModel