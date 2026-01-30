unit SIP_GUI;

interface

uses
  Winapi.Windows, Winapi.Messages, System.SysUtils, System.Variants,
  System.Classes, Vcl.Graphics,
  Vcl.Controls, Vcl.Forms, Vcl.Dialogs, Vcl.Imaging.pngimage, Vcl.Imaging.jpeg, Vcl.StdCtrls, Vcl.ExtCtrls, ShellApi;

type
  TForm1 = class(TForm)
    btnTop: TButton;
    btnFront: TButton;
    btnRight: TButton;
    pnlPreview: TPanel;
    Image4: TImage;
    lblPreview: TLabel;
    btnGenerate: TButton;
    pnlFrontView: TPanel;
    imgFront: TImage;
    pnlTopView: TPanel;
    pnlRightView: TPanel;
    imgTop: TImage;
    imgSide: TImage;
    lblTitle: TLabel;
    Name: TEdit;
    SavePath: TEdit;
    lblSavePath: TLabel;
    lblName: TLabel;
    procedure btnFrontClick(Sender: TObject);
    procedure btnTopClick(Sender: TObject);
    procedure btnRightClick(Sender: TObject);
    procedure btnGenerateClick(Sender: TObject);
  private
    var
      sImgPathTopView, sImgPathFrontView, sImgPathRightView : String;
  public
    { Public declarations }
  end;

var
  Form1: TForm1;

implementation

{$R *.dfm}

procedure TForm1.btnFrontClick(Sender: TObject);
var
  OpenDialog: TOpenDialog;
begin
  OpenDialog := TOpenDialog.Create(nil);
  try

    OpenDialog.Filter := 'Image files|*.png;*.jpg;*.jpeg;*.bmp';
    OpenDialog.Options := [ofFileMustExist];

    if OpenDialog.Execute then
    begin
      imgFront.Picture.LoadFromFile(OpenDialog.FileName);
      imgFront.Center := True;
      imgFront.Stretch := True;
      sImgPathFrontView := OpenDialog.FileName;
    end;
  finally
    OpenDialog.Free;
  end;

end;

procedure TForm1.btnGenerateClick(Sender: TObject);
begin
  // Run an executable with parameters
  ShellExecute(0, 'open', 'python.exe', 'C:\Not_Onedrive\GitHub\SIP-Project-2026\Python\V3.py 0 C:\Not_Onedrive\GitHub\SIP-Project-2026\Python\Images\square_30x30_filled.png C:\Not_Onedrive\GitHub\SIP-Project-2026\Python\Images\square_30x30_filled.png C:\Not_Onedrive\GitHub\SIP-Project-2026\Python\Images\square_30x30_filled.png test_cmd_003 C:\Users\ewanc\Downloads', nil, SW_SHOWNORMAL);

end;

procedure TForm1.btnRightClick(Sender: TObject);
var
  OpenDialog: TOpenDialog;
begin
  OpenDialog := TOpenDialog.Create(nil);
  try

    OpenDialog.Filter := 'Image files|*.png;*.jpg;*.jpeg;*.bmp';
    OpenDialog.Options := [ofFileMustExist];

    if OpenDialog.Execute then
    begin
      imgSide.Picture.LoadFromFile(OpenDialog.FileName);
      imgSide.Center := True;
      imgSide.Stretch := True;
      sImgPathRightView := OpenDialog.FileName;
    end;
  finally
    OpenDialog.Free;
  end;

end;

procedure TForm1.btnTopClick(Sender: TObject);
var
  OpenDialog: TOpenDialog;
begin
  OpenDialog := TOpenDialog.Create(nil);
  try

    OpenDialog.Filter := 'Image files|*.png;*.jpg;*.jpeg;*.bmp';
    OpenDialog.Options := [ofFileMustExist];

    if OpenDialog.Execute then
    begin
      imgTop.Picture.LoadFromFile(OpenDialog.FileName);
      imgTop.Center := True;
      imgTop.Stretch := True;
      sImgPathTopView := OpenDialog.FileName;
    end;
  finally
    OpenDialog.Free;
  end;

end;

end.
