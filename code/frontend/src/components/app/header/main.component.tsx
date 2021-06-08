import React from "react";
import AppBar from "@material-ui/core/AppBar";
import { Link, useHistory } from "react-router-dom";
import logo from "../../../resources/images/logo.png";
import { StyledToolbar } from "./styles";
import LanguageChanger from "./languageChanger";
import Button from "@material-ui/core/Button";
import { useTranslation } from "react-i18next";
import SettingsComponent from "./settings/main.component";
import WorkspaceChanger from "./workspaceChanger";
import SettingsDialog from "./settings/dialog.component";

const Header: React.FC = () => {
  const { t } = useTranslation();
  const history = useHistory();
  const goto = (path: string) => () => {
    if (history.location.pathname != path) history.push(path);
  };
  return (
    <React.Fragment>
      <AppBar position="fixed">
        <StyledToolbar>
          <Link to="/" style={{ marginRight: "1rem" }} className="no-highlight">
            <img src={logo} style={{ height: "2rem", marginRight: "1rem" }} />
          </Link>
          <Button color="inherit" onClick={goto("/dashboard")}>
            {t("header.dashboard")}
          </Button>
          <Button color="inherit" onClick={goto("/data-management")}>
            {t("header.data")}
          </Button>
          <Button color="inherit" onClick={goto("/ontology-management")}>
            {t("header.ontology")}
          </Button>
          <Button color="inherit" onClick={goto("/workflow")}>
            {t("header.workflow")}
          </Button>
          <div style={{ flexGrow: 1 }} />
          <WorkspaceChanger />
          <LanguageChanger />
          <SettingsComponent />
        </StyledToolbar>
      </AppBar>
      <StyledToolbar />
      <SettingsDialog />
    </React.Fragment>
  );
};

export default Header;
