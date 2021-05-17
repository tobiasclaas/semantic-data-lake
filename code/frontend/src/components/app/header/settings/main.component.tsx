import React from 'react';
import IconButton from '@material-ui/core/IconButton';
import SettingsIcon from '@material-ui/icons/Settings';
import settingsDialogStore from '../../../../stores/settings.store';

const SettingsComponent: React.FC = () => {
    return (
        <React.Fragment>
            <IconButton
                color="inherit"
                onClick={() => settingsDialogStore.open()}
                edge='end'
            >
                <SettingsIcon />
            </IconButton>
        </React.Fragment>
    );
}

export default SettingsComponent