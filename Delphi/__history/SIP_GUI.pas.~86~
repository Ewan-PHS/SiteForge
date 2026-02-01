unit SIP_GUI;

interface

uses
  Winapi.Windows, Winapi.Messages, System.SysUtils, System.Variants,
  System.Classes, Vcl.Graphics,
  Vcl.Controls, Vcl.Forms, Vcl.Dialogs, Vcl.Imaging.pngimage, Vcl.Imaging.jpeg, Vcl.StdCtrls, Vcl.ExtCtrls,
  ShellApi, FileCtrl, System.IOUtils;

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
    lblTitle: TLabel;
    edtName: TEdit;
    lblName: TLabel;
    bntSelectPath: TButton;
    tmr10ms: TTimer;
    procedure btnFrontClick(Sender: TObject);
    procedure btnTopClick(Sender: TObject);
    procedure btnRightClick(Sender: TObject);
    procedure btnGenerateClick(Sender: TObject);
    procedure bntSelectPathClick(Sender: TObject);
    procedure tmr10msTimer(Sender: TObject);
    procedure FormCreate(Sender: TObject);
  private
    var
      sImgPathTopView, sImgPathFrontView, sImgPathRightView, sSavePath, sName, sSiteForgePath : String;

    function OpenImageFileSelect(): String;
    function ShellExecute_AndWait(FileName: string; Params: string): bool;
  public
    { Public declarations }
  end;

var
  frmMain: TfrmMain;

implementation

{$R *.dfm}

function TfrmMain.OpenImageFileSelect(): String;
var
  OpenDialog: TOpenDialog;
begin
  OpenDialog := TOpenDialog.Create(nil);
  try
    OpenDialog.Filter := 'Image files|*.png;*.jpg;*.jpeg;*.bmp';
    OpenDialog.Options := [ofFileMustExist];

    if OpenDialog.Execute then
    begin
      Result := OpenDialog.FileName;
    end;
  finally
    OpenDialog.Free;
  end;

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
  sFilePath := OpenImageFileSelect();

  imgSide.Picture.LoadFromFile(sFilePath);
  imgSide.Center := True;
  imgSide.Stretch := True;
  sImgPathRightView := sFilePath;

end;

procedure TfrmMain.btnTopClick(Sender: TObject);
var
  sFilePath: String;
begin
  sFilePath := OpenImageFileSelect();

  imgTop.Picture.LoadFromFile(sFilePath);
  imgTop.Center := True;
  imgTop.Stretch := True;
  sImgPathTopView := sFilePath;

end;

procedure TfrmMain.btnFrontClick(Sender: TObject);
var
  sFilePath: String;
begin
  sFilePath := OpenImageFileSelect();

  imgFront.Picture.LoadFromFile(sFilePath);
  imgFront.Center := True;
  imgFront.Stretch := True;
  sImgPathFrontView := sFilePath;

end;

procedure TfrmMain.bntSelectPathClick(Sender: TObject);
var
  ChosenDirectory: string;
begin
  // Show dialog starting from C:\, with custom title
  if SelectDirectory('Select a Folder', 'C:\', ChosenDirectory) then
  begin
    ShowMessage('Selected: ' + ChosenDirectory);
    sSavePath := ChosenDirectory;
  end
  else
    ShowMessage('Selection cancelled');

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
  sSiteForgePath := TPath.GetHomePath;
  Delete(sSiteForgePath, Length(sSiteForgePath) - 6, 7);
  sSiteForgePath := sSiteForgePath + 'Local\SiteForge';
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
