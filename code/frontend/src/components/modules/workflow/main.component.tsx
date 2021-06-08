import React from 'react'
import { observer } from 'mobx-react-lite'
import ViewModel from './viewModel'
import IViewProps from '../../../models/iViewProps'
import { useTranslation } from 'react-i18next'
import workspacesStore from '../../../stores/workspaces.store'
import Sidebar from './sidebar'
import { useLocalObservable } from 'mobx-react-lite'


const elements = [
    { id: '1', data: { label: 'Node 1' }, position: { x: 250, y: 5 } },
    // you can also pass a React component as a label
    { id: '2', data: { label: <div>Node 2</div> }, position: { x: 100, y: 100 } },
    { id: 'e1-2', source: '1', target: '2', animated: true },
];
const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
    const { t } = useTranslation()
    return null
    return (
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <div style={{ flex: 1 }}>

            </div>
            <Sidebar viewModel={viewModel} />
        </div>
    )
})

export default Main
