unit SIP_GUI;

interface

uses
  Winapi.Windows, Winapi.Messages, System.SysUtils, System.Variants,
  System.Classes, Vcl.Graphics,
  Vcl.Controls, Vcl.Forms, Vcl.Dialogs, Vcl.Imaging.pngimage, Vcl.Imaging.jpeg, Vcl.StdCtrls, Vcl.ExtCtrls;

type
  TForm1 = class(TForm)
    btnTop: TButton;
    btnFront: TButton;
    btnSide: TButton;
    pnlPreview: TPanel;
    Image4: TImage;
    lblPreview: TLabel;
    btnGenerate: TButton;
    Panel1: TPanel;
    imgFront: TImage;
    Panel2: TPanel;
    Panel3: TPanel;
    imgTop: TImage;
    imgSide: TImage;
    Label1: TLabel;
    procedure btnFrontClick(Sender: TObject);
    procedure btnTopClick(Sender: TObject);
    procedure btnSideClick(Sender: TObject);
  private
    { Private declarations }
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
    end;
  finally
    OpenDialog.Free;
  end;

end;

procedure TForm1.btnSideClick(Sender: TObject);
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
    end;
  finally
    OpenDialog.Free;
  end;

end;

end.
