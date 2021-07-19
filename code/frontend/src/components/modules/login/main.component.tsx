import React from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import IViewProps from "../../../models/iViewProps";
import { useTranslation } from "react-i18next";
import TextField from "@material-ui/core/TextField";
import Card from "@material-ui/core/Card";
import Grid from "@material-ui/core/Grid";
import CardContent from "@material-ui/core/CardContent";
import Button from "@material-ui/core/Button";

const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const { t } = useTranslation();

  return (
    <Card>
      <CardContent>
        <Grid container direction="column" spacing={5}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              value={viewModel.username}
              label={t("login.username")}
              onChange={(e) => viewModel.setUsername(e.target.value)}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              type="password"
              label={t("login.password")}
              value={viewModel.password}
              onChange={(e) => viewModel.setPassword(e.target.value)}
            />
          </Grid>

          <Grid item xs={12}>
            <Button
              fullWidth
              disabled={!viewModel.canLogin}
              color="primary"
              onClick={() => viewModel.login()}
            >
              {t("generic.login")}
            </Button>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
});

export default Main;
