import React, { useEffect } from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import IViewProps from "../../../models/iViewProps";
import { useTranslation } from "react-i18next";
import TopRightFab from "../../common/topRightFab";
import AddIcon from "@material-ui/icons/Add";
import Dialog from "@material-ui/core/Dialog";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogContent from "@material-ui/core/DialogContent";
import TextField from "@material-ui/core/TextField";
import DialogActions from "@material-ui/core/DialogActions";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import { ContainerGrid } from "./styles";
import Item from "../../common/item";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import { DatamartStatus, DatamartType } from "../../../models/datamarts";
import InputLabel from "@material-ui/core/InputLabel";
import FormControl from "@material-ui/core/FormControl";
import Grid from "@material-ui/core/Grid";
import LocalOfferIcon from "@material-ui/icons/LocalOffer";
import ItemButton from "../../common/item/button";
import { blue, green } from "@material-ui/core/colors";
import AppBar from "@material-ui/core/AppBar";
import IconButton from "@material-ui/core/IconButton";
import Close from "@material-ui/icons/Close";
import Box from "@material-ui/core/Box";
import { StyledToolbar } from "../../app/header/styles";
import { SlideProps } from "@material-ui/core/Slide";
import Slide from "@material-ui/core/Slide";
import Chip from "@material-ui/core/Chip";
import { red } from "@material-ui/core/colors";
import DataViewViewModel from "./data-view";
import AnnotationViewModel from "./annotation";
import VisibilityIcon from "@material-ui/icons/Visibility";

const Transition = React.forwardRef((props: SlideProps, ref) => (
  <Slide direction="up" ref={ref} {...props} />
));

const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const { t } = useTranslation();
  useEffect(() => {
    viewModel.registerIntevals();
    return () => viewModel.deregisterIntevals();
  });

  return (
    <React.Fragment>
      <TopRightFab
        variant="extended"
        color="primary"
        onClick={() => viewModel.openUploadDialog()}
      >
        <AddIcon />
        {t("generic.add_new")}
      </TopRightFab>
      <Typography variant="h6">{t("dataset_management.title")}</Typography>
      <Typography variant="subtitle1">
        {t("dataset_management.description")}
      </Typography>
      <ContainerGrid container spacing={0}>
        {viewModel.datamarts.map((item) => (
          <Item
            key={item.uid}
            title={item.humanReadableName}
            onDelete={() => viewModel.delete(item)}
          >
            {item.status.state == DatamartStatus.failed && (
              <div
                style={{
                  flex: 1,
                  display: "flex",
                  justifyContent: "center",
                }}
              >
                <Chip
                  style={{
                    opacity: 0.8,
                    backgroundColor: red[500],
                    color: "#fff",
                    height: "auto",
                  }}
                  label={t("dataset_management.status." + item.status.state)}
                />
              </div>
            )}
            {item.status.state == DatamartStatus.running && (
              <div
                style={{
                  flex: 1,
                  display: "flex",
                  justifyContent: "center",
                }}
              >
                <Chip
                  style={{
                    opacity: 0.8,
                    backgroundColor: green[500],
                    color: "#fff",
                    height: "auto",
                  }}
                  label={t("dataset_management.status." + item.status.state)}
                />
              </div>
            )}
            {item.status.state == DatamartStatus.success && (
              <React.Fragment>
                <ItemButton
                  htmlColor={blue[500]}
                  onClick={() =>
                    viewModel.setDialogViewModel(new DataViewViewModel(item))
                  }
                >
                  <VisibilityIcon fontSize="small" />
                </ItemButton>
                <ItemButton
                  htmlColor={green[500]}
                  onClick={() =>
                    viewModel.setDialogViewModel(new AnnotationViewModel(item))
                  }
                >
                  <LocalOfferIcon fontSize="small" />
                </ItemButton>
              </React.Fragment>
            )}
          </Item>
        ))}
      </ContainerGrid>
      <Dialog
        maxWidth="sm"
        fullWidth
        open={viewModel.isUploadDialogOpen}
        disableAutoFocus
        onClose={() => viewModel.closeUploadDialog()}
      >
        <DialogTitle>{t("dataset_management.upload.title")}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            {t("dataset_management.upload.description")}
          </DialogContentText>
          <Grid container direction="column">
            <Grid container spacing={2} item>
              <Grid item sm>
                <TextField
                  fullWidth
                  autoFocus
                  onChange={(e) => viewModel.setUploadName(e.target.value)}
                  value={viewModel.uploadName}
                  margin="dense"
                  label={t("generic.name")}
                />
              </Grid>
              <Grid item sm>
                <FormControl fullWidth margin="dense">
                  <InputLabel id="demo-simple-select-label">
                    {t("dataset_management.upload.type")}
                  </InputLabel>
                  <Select
                    value={viewModel.uploadType}
                    onChange={(e) =>
                      viewModel.setUploadType(e.target.value as DatamartType)
                    }
                  >
                    <MenuItem value="csv">CSV</MenuItem>
                    <MenuItem value="json">JSON</MenuItem>
                    <MenuItem value="xml">XML</MenuItem>
                    <MenuItem value="postgresql">PostgreSQL</MenuItem>
                    <MenuItem value="mongodb">MongoDB</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
            {viewModel.bodyView}
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button color="primary" onClick={() => viewModel.closeUploadDialog()}>
            {t("generic.cancel")}
          </Button>
          <Button
            color="primary"
            disabled={!viewModel.canUpload}
            onClick={() => viewModel.upload()}
          >
            {t("generic.upload")}
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog
        fullScreen
        open={viewModel.isDialogOpen}
        TransitionComponent={Transition}
        keepMounted
      >
        <AppBar position="fixed">
          <StyledToolbar>
            <IconButton
              style={{ marginRight: "0.5rem" }}
              edge="start"
              color="inherit"
              onClick={() => viewModel.closeDialog()}
            >
              <Close />
            </IconButton>
          </StyledToolbar>
        </AppBar>
        <Box display="flex" flexDirection="column" height="100%">
          <StyledToolbar />
          <Box flexGrow={1} overflow="auto">
            {viewModel.dialogView}
          </Box>
        </Box>
      </Dialog>
    </React.Fragment>
  );
});

export default Main;
