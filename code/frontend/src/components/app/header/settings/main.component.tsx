import React from "react";
import IconButton from "@material-ui/core/IconButton";
import SettingsIcon from "@material-ui/icons/Settings";
import settingsDialogStore from "../../../../stores/settings.store";
import appStore from "../../../../stores/app.store";
import routingStore from "../../../../stores/routing.store";
import ExitToAppIcon from "@material-ui/icons/ExitToApp";
import { observer } from "mobx-react";

const SettingsComponent: React.FC = observer(() => {
  if (!appStore.isLoggedIn) return null;

  return (
    <React.Fragment>
      <IconButton
        color="inherit"
        onClick={() => routingStore.history.push("/login")}
      >
        <ExitToAppIcon />
      </IconButton>
      <IconButton
        color="inherit"
        onClick={() => settingsDialogStore.open()}
        edge="end"
      >
        <SettingsIcon />
      </IconButton>
    </React.Fragment>
  );
});

export default SettingsComponent;
