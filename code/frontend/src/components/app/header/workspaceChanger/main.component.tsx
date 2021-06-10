import React from "react";
import Button from "@material-ui/core/Button";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import FolderSpecialIcon from "@material-ui/icons/FolderSpecial";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import { observer, useLocalObservable } from "mobx-react";
import AddIcon from "@material-ui/icons/Add";
import Typography from "@material-ui/core/Typography";
import { useTheme } from "@material-ui/core/styles";
import Divider from "@material-ui/core/Divider";
import { useTranslation } from "react-i18next";
import TextField from "@material-ui/core/TextField";
import Dialog from "@material-ui/core/Dialog";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogContent from "@material-ui/core/DialogContent";
import DialogActions from "@material-ui/core/DialogActions";
import ViewModel from "./viewModel";
import workspacesStore from "../../../../stores/workspaces.store";

const WorkspaceChanger: React.FC = observer(() => {
  const viewModel = useLocalObservable(() => new ViewModel());
  const theme = useTheme();
  const { t } = useTranslation();

  return (
    <React.Fragment>
      <Button
        aria-haspopup="true"
        color="inherit"
        startIcon={<FolderSpecialIcon />}
        endIcon={<ExpandMoreIcon />}
        onClick={(event) => viewModel.setAnchorEl(event.currentTarget)}
      >
        {workspacesStore.currentWorkspace?.name}
      </Button>
      <Menu
        anchorEl={viewModel.anchorEl}
        keepMounted
        open={viewModel.isMenuOpen}
        onClose={() => viewModel.closeMenu()}
      >
        {workspacesStore.workspaces.map((item) => (
          <MenuItem
            key={item.id}
            onClick={() => viewModel.changeWorkspace(item)}
          >
            {item.name}
          </MenuItem>
        ))}
        <Divider style={{ margin: theme.spacing(1, 0) }} />

        <MenuItem onClick={() => viewModel.openDialog()}>
          <AddIcon fontSize="small" style={{ marginRight: theme.spacing(1) }} />
          <Typography variant="inherit">{t("generic.add_new")}</Typography>
        </MenuItem>
      </Menu>
      <Dialog
        open={viewModel.isDialogOpen}
        disableAutoFocus
        onClose={() => viewModel.closeDialog()}
      >
        <DialogTitle>{t("workspaceChanger.title")}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            {t("workspaceChanger.description")}
          </DialogContentText>
          <TextField
            autoFocus
            onChange={(e) => viewModel.setWorkspaceName(e.target.value)}
            value={viewModel.workspaceName}
            margin="dense"
            label="Name"
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button color="primary" onClick={() => viewModel.closeDialog()}>
            {t("generic.cancel")}
          </Button>
          <Button color="primary" onClick={() => viewModel.addNewWorkspace()}>
            {t("generic.create")}
          </Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
});

export default WorkspaceChanger;
