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
    <Card style={{ width: "20rem", margin: "0 auto" }}>
      <CardContent>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            viewModel.login();
          }}
        >
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
                type="submit"
                variant="contained"
                disabled={!viewModel.canLogin}
                color="primary"
              >
                {t("generic.login")}
              </Button>
            </Grid>
          </Grid>
        </form>
      </CardContent>
    </Card>
  );
});

export default Main;
