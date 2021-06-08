import React from "react";
import { Switch, Route, useLocation } from "react-router-dom";
import { Router } from "react-router";

import Header from "./header";
import Container from "@material-ui/core/Container";
import Backdrop from "@material-ui/core/Backdrop";
import CircularProgress from "@material-ui/core/CircularProgress";
import { useTheme } from "@material-ui/core/styles";
import { useEffect } from "react";
import ContentStore from "../../models/contentStore";
import appStore from "../../stores/app.store";
import StoreStatus from "../../models/storeStatus.enum";
import Footer from "./footer";
import { observer } from "mobx-react";
import { createHashHistory } from "history";
import { syncHistoryWithStore } from "mobx-react-router";
import routingStore from "../../stores/routing.store";
import workspacesStore from "../../stores/workspaces.store";

const RoutingComponent: React.FC = observer(() => {
  const location = useLocation();
  const theme = useTheme();
  useEffect(() => {
    assignViewModel(location.pathname);
  }, [location.pathname, workspacesStore.currentWorkspace]);

  const assignViewModel = async (path: string) => {
    await import("../modules" + path).then((res) =>
      appStore.setContentViewModel(new res.default() as ContentStore)
    );
    //.catch(() => appStore.setContentViewModel(new NotFoundStore(path)));
  };

  return (
    <div
      style={{
        flex: 1,
        position: "relative",
        display: "flex",
        flexDirection: "column",
        alignItems: "stretch",
        overflow: "auto",
      }}
    >
      <div
        style={{
          flex: 1,
          position: "relative",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Backdrop
          style={{
            position: "absolute",
            zIndex: theme.zIndex.drawer + 1,
            backgroundColor: "rgba(255,255,255,0.4)",
          }}
          open={
            appStore.contentViewModel != null &&
            (appStore.contentViewModel.status == StoreStatus.initializing ||
              appStore.contentViewModel.status == StoreStatus.working)
          }
        >
          <CircularProgress
            style={{
              position: "fixed",
              top: "50%",
            }}
          />
        </Backdrop>

        {appStore.isFullscreen ? (
          <div
            style={{
              position: "relative",
              flex: 1,
              display: "flex",
              flexDirection: "column",
            }}
          >
            {appStore.view}
          </div>
        ) : (
          <Container
            style={{
              marginTop: "2rem",
              marginBottom: "2rem",
              position: "relative",
              display: "flex",
              flexDirection: "column",
              flex: 1,
            }}
          >
            <div
              style={{
                position: "relative",
                flex: 1,
                display: "flex",
                flexDirection: "column",
              }}
            >
              {appStore.view}
            </div>
          </Container>
        )}
      </div>
      <Footer />
    </div>
  );
});

const App: React.FC = () => {
  const browserHistory = createHashHistory() as any;
  const history = syncHistoryWithStore(browserHistory, routingStore);

  return (
    <Router history={history}>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          position: "absolute",
          inset: 0,
        }}
      >
        <Header />
        <Switch>
          <Route component={RoutingComponent} />
        </Switch>
      </div>
    </Router>
  );
};

export default App;
