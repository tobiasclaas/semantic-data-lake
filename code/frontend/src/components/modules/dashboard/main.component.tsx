import React from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import IViewProps from "../../../models/iViewProps";
import { useTranslation } from "react-i18next";
import workspacesStore from "../../../stores/workspaces.store";

const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const { t } = useTranslation();

  return (
    <div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
      <div>
        {" "}
        {`${t("dashboard.welcome_message")} to ${
          workspacesStore.currentWorkspace?.name
        }`}
      </div>
    </div>
  );
});

export default Main;
