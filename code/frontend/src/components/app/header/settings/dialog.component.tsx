import React from "react"
import { observer } from "mobx-react"
import Dialog from "@material-ui/core/Dialog"
import DialogContent from "@material-ui/core/DialogContent"
import Grid from "@material-ui/core/Grid"
import DialogActions from "@material-ui/core/DialogActions"
import TableContainer from "@material-ui/core/TableContainer"
import TableRow from "@material-ui/core/TableRow"
import TableBody from "@material-ui/core/TableBody"
import Select from "@material-ui/core/Select"
import MenuItem from "@material-ui/core/MenuItem"
import Tabs from "@material-ui/core/Tabs"
import Tab from "@material-ui/core/Tab"
import Box from "@material-ui/core/Box"
import AppBar from "@material-ui/core/AppBar"
import CircularProgress from "@material-ui/core/CircularProgress"
import Button from "@material-ui/core/Button"
import settingsDialogStore, { DisplayMode } from "../../../../stores/settings.store"
import { PadlessDialogTitle, StyledBackdrop } from "./styles"
import { useTranslation } from "react-i18next"
import StoreStatus from "../../../../models/storeStatus.enum"
import List from "@material-ui/core/List"
import appStore from "../../../../stores/app.store"
import ListItem from "@material-ui/core/ListItem"
import ListItemText from "@material-ui/core/ListItemText"
import ListItemSecondaryAction from "@material-ui/core/ListItemSecondaryAction"
import IconButton from "@material-ui/core/IconButton"
import DeleteIcon from '@material-ui/icons/Delete'
import workspacesStore from "../../../../stores/workspaces.store"

const SettingsDialog: React.FC = observer(() => {
    const { t } = useTranslation()

    return (
        <Dialog
            fullWidth
            keepMounted
            disableAutoFocus
            onClose={() => settingsDialogStore.close()}
            open={settingsDialogStore.isOpen}>
            <PadlessDialogTitle>
                <AppBar position="static" color="primary">
                    <Tabs
                        value={settingsDialogStore.displayMode}
                        variant="fullWidth"
                        onChange={(_, newValue: DisplayMode) => settingsDialogStore.setDisplayMode(newValue)}
                    >
                        <Tab
                            disabled={settingsDialogStore.status === StoreStatus.working}
                            label={t("settings.primary")}
                            value={DisplayMode.primary} />
                        <Tab
                            disabled={settingsDialogStore.status === StoreStatus.working}
                            label={t("settings.workspaces")}
                            value={DisplayMode.workspaces}
                        />
                    </Tabs>
                </AppBar>
            </PadlessDialogTitle>
            <DialogContent>
                <StyledBackdrop open={settingsDialogStore.status === StoreStatus.working}>
                    <CircularProgress color="inherit" />
                </StyledBackdrop>

                <Box hidden={settingsDialogStore.displayMode !== DisplayMode.primary} position='relative'>

                </Box>
                <Box hidden={settingsDialogStore.displayMode !== DisplayMode.workspaces} position='relative'>
                    <List>
                        {
                            workspacesStore.workspaces.slice().map((item) => (
                                <ListItem key={item.id}>
                                    <ListItemText
                                        primary={item.name}
                                        secondary={workspacesStore.currentWorkspace?.id == item.id ? t('settings.current_workspace') : undefined}
                                    />
                                    <ListItemSecondaryAction>
                                        <IconButton disabled={workspacesStore.currentWorkspace?.id == item.id} edge="end" aria-label="delete" onClick={() => workspacesStore.deleteWorkspace(item)}>
                                            <DeleteIcon />
                                        </IconButton>
                                    </ListItemSecondaryAction>
                                </ListItem>)
                            )}
                    </List>
                </Box>

            </DialogContent>
            <DialogActions>
                <Button
                    variant='text'
                    onClick={() => settingsDialogStore.close()}
                    disabled={settingsDialogStore.status === StoreStatus.working}
                >
                    {t("generic.back")}
                </Button>
            </DialogActions>
        </Dialog >
    )
})

export default SettingsDialog
