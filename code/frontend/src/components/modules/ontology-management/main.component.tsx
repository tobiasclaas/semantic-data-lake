import React from "react";
import { get, set, observable, values, toJS } from "mobx"
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import IViewProps from "../../../models/iViewProps";
import { useTranslation } from "react-i18next";
import TopRightFab from "../../common/topRightFab";
import AddIcon from "@material-ui/icons/Add";
import Dialog from "@material-ui/core/Dialog";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogContent from "@material-ui/core/DialogContent";
import TextField from "@material-ui/core/TextField";
import DialogActions from "@material-ui/core/DialogActions";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import { ContainerGrid } from "./styles";
import FileInput from "../../common/FileInput";
import Item from "../../common/item";

/* Sayeds Part */
import Grid from "@material-ui/core/Grid";
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Box from '@material-ui/core/Box';
import Checkbox from "@material-ui/core/Checkbox";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import { PagesSharp } from "@material-ui/icons";

interface TabPanelProps {
  children?: React.ReactNode;
  index: any;
  value: any;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box p={3}>
          <Typography component={'span'}>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

function a11yProps(index: any) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}
function QueryTable(props) {
  const Data = props.Data;
  const Querysent = props.Querysent;
  if (Querysent == true) {
    console.log("DatatoJS", Data)
    console.log("DatatoJS", get(Data))
    console.log("DatatoJS", values(Data))
    console.log("DatatoJS", toJS(Data))
    console.log("DatatoJS", toJS(Data.slice()))
    console.log("Querysent", Querysent)
    return (<div>
      <table className="tat">
        <tbody>
          <tr><th>Subject</th><th>Predicate</th><th>Object</th></tr>
          {
            Data.map((dynamicData) =>
              <tr className="trow">
                <td>  {dynamicData.s.value}</td>
                <td> {dynamicData.p.value} </td>
                <td> {dynamicData.o.value} </td>
              </tr>
            )}
        </tbody>
      </table>
    </div>)
  } else { return null }
}

/* Sayeds Part End */

const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {


  const { t } = useTranslation();

  const [value, setValue] = React.useState(0);

  const handleChange = (event: React.ChangeEvent<{}>, newValue: number) => {
    setValue(newValue);
  };


  return (
    <React.Fragment>
      <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
        <Tab label=" Upload an Ontology-File " {...a11yProps(0)} />
        <Tab label=" Query an Ontology " {...a11yProps(1)} />
      </Tabs>
      <TabPanel value={value} index={0}>
        <TopRightFab
          variant="extended"
          color="primary"
          onClick={() => viewModel.openUploadDialog()}
        >
          <AddIcon />
          {t("generic.add_new")}
        </TopRightFab>
        <Typography variant="h6">{t("ontology_management.title")}</Typography>
        <Typography variant="subtitle1">
          {t("ontology_management.description")}
        </Typography>
        <ContainerGrid container spacing={0}>
          {viewModel.ontologies.map((item) => (
            <Item
              key={item.id}
              title={item.name}
              onDelete={() => viewModel.delete(item)}
            />
          ))}
        </ContainerGrid>
        <Dialog
          open={viewModel.isUploadDialogOpen}
          disableAutoFocus
          onClose={() => viewModel.closeUploadDialog()}
        >
          <DialogTitle>{t("ontology_management.upload.title")}</DialogTitle>
          <DialogContent>
            <DialogContentText>
              {t("ontology_management.upload.description")}
            </DialogContentText>
            <TextField
              autoFocus
              onChange={(e) => viewModel.setUploadName(e.target.value)}
              value={viewModel.uploadName}
              margin="dense"
              label={t("generic.name")}
              fullWidth
            />
            <FileInput
              label={t("generic.file")}
              accept=".owl"
              onChange={(v) => viewModel.setUploadFile(v)}
            />
          </DialogContent>
          <DialogActions>
            <Button color="primary" onClick={() => viewModel.closeUploadDialog()}>
              {t("generic.cancel")}
            </Button>
            <Button
              color="primary"
              disabled={!viewModel.canUpload}
              onClick={() => viewModel.upload()}
            >
              {t("generic.upload")}
            </Button>
          </DialogActions>
        </Dialog>
      </TabPanel>
      <TabPanel value={value} index={1}>
        <Grid item sm>
          <TextField
            autoFocus
            onChange={(e) => viewModel.setQueryString(e.target.value)}
            value={viewModel.QueryString}
            margin="dense"
            label={"Query"}
            fullWidth
          />
          <TextField
            autoFocus
            onChange={(e) => viewModel.setGraphName(e.target.value)}
            value={viewModel.GraphName}
            margin="dense"
            label={"Graph"}
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={viewModel.IsQuery}
                color="primary"
                onChange={(e) => viewModel.setIsQuery(e.target.checked)}
              />
            }
            label={t("Is Query")}
          />
          <Button
            color="primary"
            onClick={() => viewModel.query()}
          >
            {t("Send")}
          </Button>
        </Grid>
        <div>
          Here the Query should be displayed as a table, but how to do that ?!
          <QueryTable Querysent={viewModel.Querysent} Data={viewModel.Data} />
        </div>
      </TabPanel>
    </React.Fragment>
  );
});

export default Main;
