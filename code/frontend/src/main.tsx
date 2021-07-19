import i18n from "i18next";
import React from "react";
import ReactDOM from "react-dom";
import { initReactI18next } from "react-i18next";
import CssBaseline from "@material-ui/core/CssBaseline";
import { StylesProvider, ThemeProvider } from "@material-ui/core/styles";
import theme from "./theme";
import App from "./components/app";
import { LanguageHelper } from "./utils/helpers/languageHelper";
import { configure } from "mobx";
import { Router } from "react-router-dom";
import { createHashHistory } from "history";
import { syncHistoryWithStore } from "mobx-react-router";

// i18n
import de from "./resources/localization/de.json";
import en from "./resources/localization/en.json";
import routingStore from "./stores/routing.store";

const bootstrap = async () => {
  await i18n.use(initReactI18next).init({
    lng: LanguageHelper.defaultLanguage,
    keySeparator: false,
    nsSeparator: false,
    resources: {
      en: {
        translation: en,
      },
      de: {
        translation: de,
      },
    },
  });

  configure({ enforceActions: "observed" });
  const browserHistory = createHashHistory() as any;
  const history = syncHistoryWithStore(browserHistory, routingStore);
  history.push("/login");

  ReactDOM.render(
    <StylesProvider injectFirst>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router history={history}>
          <App />
        </Router>
      </ThemeProvider>
    </StylesProvider>,
    document.getElementById("root")
  );
};

bootstrap();
