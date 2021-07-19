import React from "react";
import IconButton from "@material-ui/core/IconButton";
import SettingsIcon from "@material-ui/icons/Settings";
import settingsDialogStore from "../../../../stores/settings.store";
import appStore from "../../../../stores/app.store";

const SettingsComponent: React.FC = () => {
  if (!appStore.isLoggedIn) return null;

  return (
    <React.Fragment>
      <IconButton
        color="inherit"
        onClick={() => settingsDialogStore.open()}
        edge="end"
      >
        <SettingsIcon />
      </IconButton>
    </React.Fragment>
  );
};

export default SettingsComponent;
