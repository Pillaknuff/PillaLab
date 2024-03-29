#############################################################################
# Generated by PAGE version 4.26
#  in conjunction with Tcl version 8.6
#  Feb 07, 2020 07:21:59 AM CET  platform: Windows NT
set vTcl(timestamp) ""


if {!$vTcl(borrow) && !$vTcl(template)} {

set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_analog) #ececec
set vTcl(actual_gui_menu_analog) #ececec
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) #d9d9d9
set vTcl(analog_color_p) #d9d9d9
set vTcl(analog_color_m) #ececec
set vTcl(active_fg) #000000
set vTcl(actual_gui_menu_active_bg)  #ececec
set vTcl(active_menu_fg) #000000
}




proc vTclWindow.top42 {base} {
    global vTcl
    if {$base == ""} {
        set base .top42
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -background $vTcl(actual_gui_bg) 
    wm focusmodel $top passive
    wm geometry $top 595x582+650+150
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 1924 1061
    wm minsize $top 120 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    wm title $top "New Toplevel"
    vTcl:DefineAlias "$top" "Toplevel1" vTcl:Toplevel:WidgetProc "" 1
    label $top.lab43 \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 14} -foreground $vTcl(actual_gui_fg) \
        -text {Mr. Map} 
    vTcl:DefineAlias "$top.lab43" "Label1" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab44 \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) -text Start 
    vTcl:DefineAlias "$top.lab44" "Label2" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab45 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text Stop 
    vTcl:DefineAlias "$top.lab45" "Label2_1" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab46 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text Step 
    vTcl:DefineAlias "$top.lab46" "Label2_2" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab47 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text theta 
    vTcl:DefineAlias "$top.lab47" "Label2_3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab48 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text x 
    vTcl:DefineAlias "$top.lab48" "Label2_4" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab49 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text y 
    vTcl:DefineAlias "$top.lab49" "Label2_5" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab50 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text z 
    vTcl:DefineAlias "$top.lab50" "Label2_6" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex63 \
        -background white -font TkTextFont -foreground black -height 24 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 84 -wrap word 
    .top42.tex63 configure -font "TkTextFont"
    .top42.tex63 insert end text
    vTcl:DefineAlias "$top.tex63" "theta_start" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex64 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 84 -wrap word 
    .top42.tex64 configure -font "TkTextFont"
    .top42.tex64 insert end text
    vTcl:DefineAlias "$top.tex64" "theta_end" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex65 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 84 -wrap word 
    .top42.tex65 configure -font "TkTextFont"
    .top42.tex65 insert end text
    vTcl:DefineAlias "$top.tex65" "theta_step" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex66 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 84 -wrap word 
    .top42.tex66 configure -font "TkTextFont"
    .top42.tex66 insert end text
    vTcl:DefineAlias "$top.tex66" "x_start" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex67 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 84 -wrap word 
    .top42.tex67 configure -font "TkTextFont"
    .top42.tex67 insert end text
    vTcl:DefineAlias "$top.tex67" "x_end" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex68 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 84 -wrap word 
    .top42.tex68 configure -font "TkTextFont"
    .top42.tex68 insert end text
    vTcl:DefineAlias "$top.tex68" "y_start" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex69 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 84 -wrap word 
    .top42.tex69 configure -font "TkTextFont"
    .top42.tex69 insert end text
    vTcl:DefineAlias "$top.tex69" "x_step" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex70 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 84 -wrap word 
    .top42.tex70 configure -font "TkTextFont"
    .top42.tex70 insert end text
    vTcl:DefineAlias "$top.tex70" "y_end" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex71 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 84 -wrap word 
    .top42.tex71 configure -font "TkTextFont"
    .top42.tex71 insert end text
    vTcl:DefineAlias "$top.tex71" "y_step" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex72 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 84 -wrap word 
    .top42.tex72 configure -font "TkTextFont"
    .top42.tex72 insert end text
    vTcl:DefineAlias "$top.tex72" "z_start" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex73 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 84 -wrap word 
    .top42.tex73 configure -font "TkTextFont"
    .top42.tex73 insert end text
    vTcl:DefineAlias "$top.tex73" "z_end" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex74 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 84 -wrap word 
    .top42.tex74 configure -font "TkTextFont"
    .top42.tex74 insert end text
    vTcl:DefineAlias "$top.tex74" "z_step" vTcl:WidgetProc "Toplevel1" 1
    ttk::combobox $top.tCo76 \
        -values {"x"} {"map"} {"follow θ"} {} -font TkTextFont \
        -textvariable theta_what -foreground {} -background {} -takefocus {} 
    vTcl:DefineAlias "$top.tCo76" "TCombobox1" vTcl:WidgetProc "Toplevel1" 1
    ttk::combobox $top.tCo77 \
        -values {"x"} {"map"} {"follow θ"} {} -font TkTextFont \
        -textvariable x_what -foreground {} -background {} -takefocus {} 
    vTcl:DefineAlias "$top.tCo77" "TCombobox1_15" vTcl:WidgetProc "Toplevel1" 1
    ttk::combobox $top.tCo78 \
        -values {"x"} {"map"} {"follow θ"} {} -font TkTextFont \
        -textvariable y_what -foreground {} -background {} -takefocus {} 
    vTcl:DefineAlias "$top.tCo78" "TCombobox1_16" vTcl:WidgetProc "Toplevel1" 1
    ttk::combobox $top.tCo79 \
        -values {"x"} {"map"} {"follow θ"} {} -font TkTextFont \
        -textvariable z_what -foreground {} -background {} -takefocus {} 
    vTcl:DefineAlias "$top.tCo79" "TCombobox1_17" vTcl:WidgetProc "Toplevel1" 1
    button $top.but80 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5f5f5f -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text Start 
    vTcl:DefineAlias "$top.but80" "Button1" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex81 \
        -background white -font TkTextFont -foreground black -height 24 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 254 -wrap word 
    .top42.tex81 configure -font "TkTextFont"
    .top42.tex81 insert end text
    vTcl:DefineAlias "$top.tex81" "folder_text" vTcl:WidgetProc "Toplevel1" 1
    button $top.but82 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5f5f5f -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text folder 
    vTcl:DefineAlias "$top.but82" "Button1_18" vTcl:WidgetProc "Toplevel1" 1
    button $top.but83 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5f5f5f -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text Pause 
    vTcl:DefineAlias "$top.but83" "Button1_19" vTcl:WidgetProc "Toplevel1" 1
    button $top.but84 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #eb0214 -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text Stop 
    vTcl:DefineAlias "$top.but84" "Button1_20" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab85 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text Steps 
    vTcl:DefineAlias "$top.lab85" "Label2_3" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex86 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 54 -wrap word 
    .top42.tex86 configure -font "TkTextFont"
    .top42.tex86 insert end text
    vTcl:DefineAlias "$top.tex86" "steps" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab87 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text Status 
    vTcl:DefineAlias "$top.lab87" "Label2_4" vTcl:WidgetProc "Toplevel1" 1
    text $top.tex88 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 434 -wrap word 
    .top42.tex88 configure -font "TkTextFont"
    .top42.tex88 insert end text
    vTcl:DefineAlias "$top.tex88" "Status_proclaimer" vTcl:WidgetProc "Toplevel1" 1
    button $top.but89 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5f5f5f -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 28} -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text X 
    vTcl:DefineAlias "$top.but89" "Button1_6" vTcl:WidgetProc "Toplevel1" 1
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.lab43 \
        -in $top -x 30 -y 30 -anchor nw -bordermode ignore 
    place $top.lab44 \
        -in $top -x 200 -y 90 -anchor nw -bordermode ignore 
    place $top.lab45 \
        -in $top -x 310 -y 90 -width 30 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.lab46 \
        -in $top -x 440 -y 90 -width 30 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.lab47 \
        -in $top -x 20 -y 160 -width 30 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.lab48 \
        -in $top -x 20 -y 200 -width 30 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.lab49 \
        -in $top -x 20 -y 240 -width 30 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.lab50 \
        -in $top -x 20 -y 280 -width 30 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.tex63 \
        -in $top -x 170 -y 160 -width 84 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.tex64 \
        -in $top -x 290 -y 160 -width 84 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex65 \
        -in $top -x 410 -y 160 -width 84 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex66 \
        -in $top -x 170 -y 200 -width 84 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex67 \
        -in $top -x 290 -y 200 -width 84 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex68 \
        -in $top -x 170 -y 240 -width 84 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex69 \
        -in $top -x 410 -y 200 -width 84 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex70 \
        -in $top -x 290 -y 240 -width 84 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex71 \
        -in $top -x 410 -y 240 -width 84 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex72 \
        -in $top -x 170 -y 280 -width 84 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex73 \
        -in $top -x 290 -y 280 -width 84 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex74 \
        -in $top -x 410 -y 280 -width 84 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tCo76 \
        -in $top -x 80 -y 160 -width 63 -relwidth 0 -height 21 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.tCo77 \
        -in $top -x 80 -y 200 -width 63 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.tCo78 \
        -in $top -x 80 -y 240 -width 63 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.tCo79 \
        -in $top -x 80 -y 280 -width 63 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.but80 \
        -in $top -x 120 -y 410 -width 67 -relwidth 0 -height 54 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.tex81 \
        -in $top -x 30 -y 350 -width 254 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but82 \
        -in $top -x 300 -y 350 -width 117 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but83 \
        -in $top -x 200 -y 410 -width 67 -height 54 -anchor nw \
        -bordermode ignore 
    place $top.but84 \
        -in $top -x 280 -y 410 -width 137 -relwidth 0 -height 54 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab85 \
        -in $top -x 540 -y 280 -width 30 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.tex86 \
        -in $top -x 520 -y 310 -width 54 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab87 \
        -in $top -x 20 -y 480 -width 80 -relwidth 0 -height 21 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.tex88 \
        -in $top -x 60 -y 510 -width 434 -relwidth 0 -height 54 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but89 \
        -in $top -x 530 -y 10 -width 57 -relwidth 0 -height 54 -relheight 0 \
        -anchor nw -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

set btop ""
if {$vTcl(borrow)} {
    set btop .bor[expr int([expr rand() * 100])]
    while {[lsearch $btop $vTcl(tops)] != -1} {
        set btop .bor[expr int([expr rand() * 100])]
    }
}
set vTcl(btop) $btop
Window show .
Window show .top42 $btop
if {$vTcl(borrow)} {
    $btop configure -background plum
}

