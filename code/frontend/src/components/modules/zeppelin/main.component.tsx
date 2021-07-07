import React from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import IViewProps from "../../../models/iViewProps";
import { useTranslation } from "react-i18next";
import Iframe from 'react-iframe'

const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const { t } = useTranslation();

  return (
    <div>
      <div>
        <iframe
          height="100%"
          width="100%"
          src="http://localhost:1234/#/&output=embed"
          title="YouTube video player"
          target="_parent"
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        >

        </iframe>
      </div>
    </div>
  );
});

export default Main;
