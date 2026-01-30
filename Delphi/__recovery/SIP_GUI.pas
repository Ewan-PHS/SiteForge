unit SIP_GUI;

interface

uses
  Winapi.Windows, Winapi.Messages, System.SysUtils, System.Variants, System.Classes, Vcl.Graphics,
  Vcl.Controls, Vcl.Forms, Vcl.Dialogs, Vcl.StdCtrls, Vcl.ExtCtrls;

type
  TForm1 = class(TForm)
    btnTop: TButton;
    Image1: TImage;
    Image2: TImage;
    btnFront: TButton;
    Image3: TImage;
    btnSide: TButton;
    pnlPreview: TPanel;
    Image4: TImage;
    lblPreview: TLabel;
    btnGenerate: TButton;
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Form1: TForm1;

implementation

{$R *.dfm}

end.
