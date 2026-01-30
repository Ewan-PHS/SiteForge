program SIP_Project;

uses
  Vcl.Forms,
  SIP_GUI in 'SIP_GUI.pas' {Form1};

{$R *.res}

begin
  Application.Initialize;
  Application.MainFormOnTaskbar := True;
  Application.CreateForm(TForm1, Form1);
  Application.Run;
end.
