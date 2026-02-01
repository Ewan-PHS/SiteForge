object frmMain: TfrmMain
  Left = 0
  Top = 0
  Caption = 'SiteForge'
  ClientHeight = 494
  ClientWidth = 680
  Color = clBtnFace
  Font.Charset = ANSI_CHARSET
  Font.Color = clWindowText
  Font.Height = -16
  Font.Name = 'Sitka Banner'
  Font.Style = []
  OnCreate = FormCreate
  TextHeight = 23
  object lblTitle: TLabel
    Left = 136
    Top = 8
    Width = 256
    Height = 92
    Caption = 'SiteForge'
    Font.Charset = ANSI_CHARSET
    Font.Color = clWindowText
    Font.Height = -64
    Font.Name = 'Sitka Heading Semibold'
    Font.Style = [fsBold, fsItalic]
    ParentFont = False
  end
  object lblName: TLabel
    Left = 167
    Top = 279
    Width = 146
    Height = 23
    Caption = 'Name to save 3D model'
  end
  object btnTop: TButton
    Left = 8
    Top = 236
    Width = 121
    Height = 25
    Caption = 'Select a top view'
    TabOrder = 0
    OnClick = btnTopClick
  end
  object btnFront: TButton
    Left = 8
    Top = 405
    Width = 121
    Height = 25
    Caption = 'Select a front view'
    TabOrder = 1
    OnClick = btnFrontClick
  end
  object btnRight: TButton
    Left = 177
    Top = 236
    Width = 121
    Height = 25
    Caption = 'Select a right view'
    TabOrder = 2
    OnClick = btnRightClick
  end
  object pnlPreview: TPanel
    Left = 336
    Top = 110
    Width = 337
    Height = 376
    TabOrder = 3
    object imgPreview3DModel: TImage
      Left = 8
      Top = 48
      Width = 321
      Height = 321
    end
    object lblPreview: TLabel
      Left = 48
      Top = 11
      Width = 243
      Height = 31
      Caption = 'Preview of 3D model'
      Font.Charset = ANSI_CHARSET
      Font.Color = clWindowText
      Font.Height = -27
      Font.Name = 'Times New Roman'
      Font.Style = [fsBold, fsUnderline]
      ParentFont = False
    end
  end
  object btnGenerate: TButton
    Left = 8
    Top = 446
    Width = 305
    Height = 40
    Caption = 'Generate 3D model'
    Font.Charset = ANSI_CHARSET
    Font.Color = clWindowText
    Font.Height = -19
    Font.Name = 'Sitka Banner'
    Font.Style = []
    ParentFont = False
    TabOrder = 4
    OnClick = btnGenerateClick
  end
  object pnlFrontView: TPanel
    Left = 8
    Top = 279
    Width = 121
    Height = 120
    TabOrder = 5
    object imgFront: TImage
      Left = 8
      Top = 8
      Width = 105
      Height = 105
    end
  end
  object pnlTopView: TPanel
    Left = 8
    Top = 110
    Width = 121
    Height = 120
    TabOrder = 6
    object imgTop: TImage
      Left = 8
      Top = 8
      Width = 105
      Height = 105
    end
  end
  object pnlRightView: TPanel
    Left = 177
    Top = 110
    Width = 121
    Height = 120
    TabOrder = 7
    object imgSide: TImage
      Left = 8
      Top = 8
      Width = 105
      Height = 105
    end
  end
  object edtName: TEdit
    Left = 160
    Top = 304
    Width = 160
    Height = 31
    TabOrder = 8
  end
  object bntSelectPath: TButton
    Left = 177
    Top = 360
    Width = 121
    Height = 32
    Caption = 'Select Save Path'
    TabOrder = 9
    OnClick = bntSelectPathClick
  end
  object tmr10ms: TTimer
    Interval = 10
    OnTimer = tmr10msTimer
    Left = 632
    Top = 16
  end
end
