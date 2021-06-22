import React from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import IViewProps from "../../../../../models/iViewProps";
import { useTranslation } from "react-i18next";
import FileInput from "../../../../common/FileInput";
import Grid from "@material-ui/core/Grid";
import { TextField } from "@material-ui/core";

const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const { t } = useTranslation();

  return (
    <React.Fragment>
      <Grid item container xs>
        <FileInput
          label={t("generic.file")}
          accept=".csv"
          onChange={(v) => viewModel.setFile(v)}
        />
      </Grid>
    </React.Fragment>
  );
});

export default Main;
