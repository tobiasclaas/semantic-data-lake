import React from "react";
import { Switch, Route } from "react-router-dom";

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
import workspacesStore from "../../stores/workspaces.store";
import routingStore from "../../stores/routing.store";
import { toJS } from "mobx";

const RoutingComponent: React.FC = observer(() => {
  const location = routingStore.history.location;
  const state = toJS(routingStore.history.location.state) ?? null;

  const theme = useTheme();
  useEffect(() => {
    assignViewModel(location.pathname);
  }, [location.pathname, workspacesStore.currentWorkspace, state]);

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
  return (
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
  );
};

export default App;
