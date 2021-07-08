import React from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import IViewProps from "../../../models/iViewProps";
import { useTranslation } from "react-i18next";
import Iframe from 'react-iframe'

const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const { t } = useTranslation();


  return (
    <div style = {{height:"100vh"}} width="1500">
        <iframe
          src="http://localhost:1234/#/"
          style = {{height:"100vh"}}
          width="1500"
          title="YouTube video player"
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        >
        </iframe>
    </div>
  );
});

export default Main;
