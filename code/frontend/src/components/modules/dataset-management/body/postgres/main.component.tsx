import React from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import IViewProps from "../../../../../models/iViewProps";
import { useTranslation } from "react-i18next";
import FileInput from "../../../../common/FileInput";
import Grid from "@material-ui/core/Grid";
import { TextField } from "@material-ui/core";
import Checkbox from "@material-ui/core/Checkbox";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';

const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const { t } = useTranslation();

  return (
    <React.Fragment>
      <Grid container spacing={2} item style={{ alignItems: "center" }}>
        <Grid item>
          <FormControlLabel
            control={
              <TextField
                fullWidth
                autoFocus
                onChange={(e) => viewModel.setHost(e.target.value)}
                value={viewModel.Host}
                margin="dense"
                label={t("dataset_management.upload.mongodb.host")}
              />
            }
          />
        </Grid>
        <Grid item>
          <FormControlLabel
            control={
              <TextField
                fullWidth
                autoFocus
                onChange={(e) => viewModel.setPort(e.target.value)}
                value={viewModel.Port}
                margin="dense"
                label={t("dataset_management.upload.mongodb.port")}
              />
            }
          />
        </Grid>
        <Grid item>
          <FormControlLabel
            control={
              <TextField
                fullWidth
                autoFocus
                onChange={(e) => viewModel.setDataBase(e.target.value)}
                value={viewModel.DataBase}
                margin="dense"
                label={t("dataset_management.upload.mongodb.database")}
              />
            }
          />
        </Grid>
        <Grid item>
          <FormControlLabel
            control={
              <TextField
                fullWidth
                autoFocus
                onChange={(e) => viewModel.setTable(e.target.value)}
                value={viewModel.Table}
                margin="dense"
                label={t("dataset_management.upload.mongodb.collection")}
              />
            }
          />
        </Grid>
        <Grid item>
          <FormControlLabel
            control={
              <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={viewModel.Target_Storage}
              onChange={(e) => viewModel.setTarget_Storage(e.target.value)}
              label={t("dataset_management.upload.mongodb.target_storage")}
            >
              <MenuItem value={"HDFS"}>HDFS</MenuItem>
              <MenuItem value={"MongoDB"}>MongoDB</MenuItem>
              <MenuItem value={"Postgres"}>Postgres</MenuItem>
              label={t("dataset_management.upload.mongodb.target_storage")}
            </Select>
            }
          />
        </Grid>
        <Grid item>
          <FormControlLabel
            control={
              <TextField
                fullWidth
                autoFocus
                onChange={(e) => viewModel.setUser(e.target.value)}
                value={viewModel.User}
                margin="dense"
                label={t("dataset_management.upload.mongodb.user")}
              />
            }
          />
        </Grid>
        <Grid item>
          <FormControlLabel
            control={
              <TextField
                fullWidth
                autoFocus
                onChange={(e) => viewModel.setPassword(e.target.value)}
                value={viewModel.Password}
                margin="dense"
                label={t("dataset_management.upload.mongodb.password")}
              />
            }
          />
        </Grid>
        <Grid item>
          <FormControlLabel
            control={
              <TextField
                fullWidth
                autoFocus
                onChange={(e) => viewModel.setUser(e.target.value)}
                value={viewModel.Comment}
                margin="dense"
                label={t("dataset_management.upload.mongodb.comment")}
              />
            }
          />
        </Grid>
      </Grid>
    </React.Fragment>
  );
});

export default Main;
