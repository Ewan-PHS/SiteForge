unit SIP_GUI;

interface

uses
  Winapi.Windows, Winapi.Messages, System.SysUtils, System.Variants,
  System.Classes, Vcl.Graphics,
  Vcl.Controls, Vcl.Forms, Vcl.Dialogs, Vcl.Imaging.pngimage, Vcl.Imaging.jpeg, Vcl.StdCtrls, Vcl.ExtCtrls,
  ShellApi, FileCtrl, System.IOUtils, Vcl.ComCtrls,
  Vcl.NumberBox;

type
  TfrmMain = class(TForm)
    btnTop: TButton;
    btnFront: TButton;
    btnRight: TButton;
    pnlPreview: TPanel;
    imgPreview3DModel: TImage;
    lblPreview: TLabel;
    btnGenerate: TButton;
    pnlFrontView: TPanel;
    imgFront: TImage;
    pnlTopView: TPanel;
    pnlRightView: TPanel;
    imgTop: TImage;
    imgSide: TImage;
    edtName: TEdit;
    lblName: TLabel;
    bntSelectPath: TButton;
    tmr10ms: TTimer;
    Shape1: TShape;
    Shape2: TShape;
    Shape3: TShape;
    Shape4: TShape;
    lblSavePathDisplay: TLabel;
    redtSavePathDisplay: TRichEdit;
    pgctrlMain: TPageControl;
    tabModelGen: TTabSheet;
    tabSlicing: TTabSheet;
    tabSettings: TTabSheet;
    pgctrlSettings: TPageControl;
    tabPrintSettings: TTabSheet;
    tabMaterialSettings: TTabSheet;
    tabPrinterSettings: TTabSheet;
    pgctrlPrintSettings: TPageControl;
    tabLayersPerimeters: TTabSheet;
    tabSpeed: TTabSheet;
    tabAdvanced: TTabSheet;
    pgctrlPrinterSettings: TPageControl;
    tabGeneralPrinter: TTabSheet;
    tabCustomGcode: TTabSheet;
    pgctrlMaterialSettings: TPageControl;
    tabGeneralMaterial: TTabSheet;
    TabSheet2: TTabSheet;
    pnlBedDimentions: TPanel;
    nobxBedShapeX: TNumberBox;
    nobxBedShapeY: TNumberBox;
    nobxBedShapeZ: TNumberBox;
    lblBedDimsCaption: TLabel;
    lblbedDimsX: TLabel;
    lblbedDimsY: TLabel;
    lblbedDimsZ: TLabel;
    pnlZOffset: TPanel;
    lblZOffsetCaption: TLabel;
    nobxZOffset: TNumberBox;
    pnlGcodeFlavor: TPanel;
    lblGcodeFlavorCaption: TLabel;
    cmbbxGcodeFlavor: TComboBox;
    tabExtruder: TTabSheet;
    pnlNozzelDiamater: TPanel;
    lblNozzelDiameterCaption: TLabel;
    nobxNozzelDiameter: TNumberBox;
    lblNozzelDiameterMeasurements: TLabel;
    Label1: TLabel;
    Label2: TLabel;
    Label3: TLabel;
    lblBedShapeXDimensions: TLabel;
    lblBedShapeYDimensions: TLabel;
    lblBedShapeZDimensions: TLabel;
    lblZOffsetDimensions: TLabel;
    pnlRetraction: TPanel;
    lblRetractionCaption: TLabel;
    lblRetractionLength: TLabel;
    lblRetractionSpeedMeasurements: TLabel;
    lblRetractionSpeed: TLabel;
    lblRetractionLengthMeasurements: TLabel;
    nobxRetractionLength: TNumberBox;
    nobxRetractionSpeed: TNumberBox;
    memPrinterGcodeStart: TMemo;
    pnlPrinterGcodeStart: TPanel;
    pnlPrinterGcodeEnd: TPanel;
    memPrinterGcodeEnd: TMemo;
    pnlPrinterGcodeBeforeLayerChange: TPanel;
    memPrinterGcodeBeforeLayerChange: TMemo;
    pnlPrinterGcodeAfterLayerChange: TPanel;
    memPrinterGcodeAfterLayerChange: TMemo;
    lblPrinterGcodeStart: TLabel;
    lblPrinterGcodeEnd: TLabel;
    lblPrinterGcodeBeforeLayerChange: TLabel;
    lblPrinterGcodeAfterLayerChange: TLabel;
    imgNameplate_Model: TImage;
    imgNameplate_Slicer: TImage;
    procedure btnFrontClick(Sender: TObject);
    procedure btnTopClick(Sender: TObject);
    procedure btnRightClick(Sender: TObject);
    procedure btnGenerateClick(Sender: TObject);
    procedure bntSelectPathClick(Sender: TObject);
    procedure tmr10msTimer(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure redtSavePathDisplayChange(Sender: TObject);
  private
    var
      sImgPathTopView, sImgPathFrontView, sImgPathRightView, sSavePath, sName, sSiteForgePath, sUserPath : String;

    function OpenImageFileSelect(sTitle : String): String;
    function ShellExecute_AndWait(FileName: string; Params: string): bool;
  public
    { Public declarations }
  end;

var
  frmMain: TfrmMain;

implementation

{$R *.dfm}

function TfrmMain.OpenImageFileSelect(sTitle : String): String;
var
  OpenDialog: TOpenDialog;
begin
  OpenDialog := TOpenDialog.Create(nil);
  try
    OpenDialog.Filter := 'Image files|*.png;*.jpg;*.jpeg;*.bmp';
    OpenDialog.Options := [ofFileMustExist];
    OpenDialog.Title := sTitle;

    if OpenDialog.Execute then
    begin
      Result := OpenDialog.FileName
    end;
  finally
    OpenDialog.Free;
  end;

end;

procedure TfrmMain.redtSavePathDisplayChange(Sender: TObject);
begin
  if redtSavePathDisplay.Text <> '' then
    sSavePath := redtSavePathDisplay.Text;
end;

function TfrmMain.ShellExecute_AndWait(FileName: string; Params: string): bool;
var
  exInfo: TShellExecuteInfo;
  Ph: DWORD;
begin

  FillChar(exInfo, SizeOf(exInfo), 0);
  with exInfo do
  begin
    cbSize := SizeOf(exInfo);
    fMask := SEE_MASK_NOCLOSEPROCESS or SEE_MASK_FLAG_DDEWAIT;
    Wnd := GetActiveWindow();
    exInfo.lpVerb := 'open';
    exInfo.lpParameters := PChar(Params);
    lpFile := PChar(FileName);
    nShow := SW_HIDE;
  end;
  if ShellExecuteEx(@exInfo) then
    Ph := exInfo.hProcess
  else
  begin
    ShowMessage(SysErrorMessage(GetLastError));
    Result := true;
    exit;
  end;
  while WaitForSingleObject(exInfo.hProcess, 50) <> WAIT_OBJECT_0 do
    Application.ProcessMessages;
  CloseHandle(Ph);

  Result := true;

end;

procedure TfrmMain.btnRightClick(Sender: TObject);
var
  sFilePath: String;
begin
  sFilePath := OpenImageFileSelect('Select a RIGHT view image');

  if sFilePath = '' then
    exit;

  imgSide.Picture.LoadFromFile(sFilePath);
  imgSide.Center := True;
  imgSide.Stretch := True;
  sImgPathRightView := sFilePath;

end;

procedure TfrmMain.btnTopClick(Sender: TObject);
var
  sFilePath: String;
begin
  sFilePath := OpenImageFileSelect('Select a TOP view image');

  if sFilePath = '' then
    exit;

  imgTop.Picture.LoadFromFile(sFilePath);
  imgTop.Center := True;
  imgTop.Stretch := True;
  sImgPathTopView := sFilePath;

end;

procedure TfrmMain.btnFrontClick(Sender: TObject);
var
  sFilePath: String;
begin
  sFilePath := OpenImageFileSelect('Select a FRONT view image');

  if sFilePath = '' then
    exit;

  imgFront.Picture.LoadFromFile(sFilePath);
  imgFront.Center := True;
  imgFront.Stretch := True;
  sImgPathFrontView := sFilePath;

end;

procedure TfrmMain.bntSelectPathClick(Sender: TObject);
var
  FileOpenDialog: TFileOpenDialog;
begin
  FileOpenDialog := TFileOpenDialog.Create(nil);
  try
    FileOpenDialog.Options := [fdoPickFolders, fdoPathMustExist];
    FileOpenDialog.Title := 'Select a Folder';
    FileOpenDialog.DefaultFolder := sUserPath;

    if FileOpenDialog.Execute then
    begin
      sSavePath := FileOpenDialog.FileName;
      redtSavePathDisplay.Text := sSavePath;
    end;
  finally
    FileOpenDialog.Free;
  end;

end;

procedure TfrmMain.btnGenerateClick(Sender: TObject);
var
  sPythonCommand, sRenderedModelPath: String;
  SEInfo: TShellExecuteInfo;
  ExitCode: DWORD;
begin
  sPythonCommand := 'C:\Not_Onedrive\GitHub\SIP-Project-2026\Python\V3.py 0';
  sPythonCommand := sPythonCommand + ' ' + sImgPathTopView;
  sPythonCommand := sPythonCommand + ' ' + sImgPathFrontView;
  sPythonCommand := sPythonCommand + ' ' + sImgPathRightView;
  sPythonCommand := sPythonCommand + ' ' + sName;
  sPythonCommand := sPythonCommand + ' ' + sSavePath;

  sRenderedModelPath := sSiteForgePath + '\renders\rendered_' + sName + '.png';

  if ShellExecute_AndWait('python.exe', sPythonCommand) then
    imgPreview3DModel.Picture.LoadFromFile(sRenderedModelPath);

end;

procedure TfrmMain.FormCreate(Sender: TObject);
begin
  sSiteForgePath := TPath.Combine(GetEnvironmentVariable('LOCALAPPDATA'), 'SiteForge');

  sUserPath := TPath.GetDownloadsPath;

  redtSavePathDisplay.Text := '';

  pgctrlMain.TabIndex := 0;

end;

procedure TfrmMain.tmr10msTimer(Sender: TObject);
begin
  sName := edtName.Text;

  if (sImgPathRightView <> '') and (sImgPathTopView <> '') and (sImgPathFrontView <> '') and (sSavePath <> '') and (edtName.Text <> '') then
    btnGenerate.Enabled := True
  else
    btnGenerate.Enabled := False;

end;

end.
