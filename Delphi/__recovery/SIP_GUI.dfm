object Form1: TForm1
  Left = 0
  Top = 0
  Caption = '<insert fitting name here>'
  ClientHeight = 494
  ClientWidth = 677
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = 'Segoe UI'
  Font.Style = []
  TextHeight = 15
  object Image1: TImage
    Left = 24
    Top = 142
    Width = 105
    Height = 105
  end
  object Image2: TImage
    Left = 24
    Top = 318
    Width = 105
    Height = 105
  end
  object Image3: TImage
    Left = 176
    Top = 142
    Width = 105
    Height = 105
  end
  object btnTop: TButton
    Left = 8
    Top = 270
    Width = 129
    Height = 25
    Caption = 'Pick a top view'
    Font.Charset = ANSI_CHARSET
    Font.Color = clWindowText
    Font.Height = -16
    Font.Name = 'Times New Roman'
    Font.Style = []
    ParentFont = False
    TabOrder = 0
  end
  object btnFront: TButton
    Left = 8
    Top = 431
    Width = 129
    Height = 25
    Caption = 'Pick a front view'
    Font.Charset = ANSI_CHARSET
    Font.Color = clWindowText
    Font.Height = -16
    Font.Name = 'Times New Roman'
    Font.Style = []
    ParentFont = False
    TabOrder = 1
  end
  object btnSide: TButton
    Left = 169
    Top = 270
    Width = 120
    Height = 25
    Caption = 'Pick a side view'
    Font.Charset = ANSI_CHARSET
    Font.Color = clWindowText
    Font.Height = -16
    Font.Name = 'Times New Roman'
    Font.Style = []
    ParentFont = False
    TabOrder = 2
  end
  object pnlPreview: TPanel
    Left = 320
    Top = 126
    Width = 355
    Height = 360
    TabOrder = 3
    object Image4: TImage
      Left = 24
      Top = 48
      Width = 297
      Height = 297
    end
    object lblPreview: TLabel
      Left = 56
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
    Left = 161
    Top = 357
    Width = 153
    Height = 58
    Caption = 'Generate 3D model'
    Font.Charset = ANSI_CHARSET
    Font.Color = clWindowText
    Font.Height = -19
    Font.Name = 'Times New Roman'
    Font.Style = []
    ParentFont = False
    TabOrder = 4
  end
end
