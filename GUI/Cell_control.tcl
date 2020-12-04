#############################################################################
# Generated by PAGE version 4.26
#  in conjunction with Tcl version 8.6
#  Feb 14, 2020 07:12:21 PM CET  platform: Windows NT
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
        -background $vTcl(actual_gui_bg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black 
    wm focusmodel $top passive
    wm geometry $top 458x980+828+29
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
    vTcl:DefineAlias "$top" "toplevel" vTcl:Toplevel:WidgetProc "" 1
    button $top.but43 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command OpenCell1 -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text Open 
    vTcl:DefineAlias "$top.but43" "open1" vTcl:WidgetProc "toplevel" 1
    button $top.but44 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command CloseCell1 -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text Close 
    vTcl:DefineAlias "$top.but44" "close1" vTcl:WidgetProc "toplevel" 1
    label $top.lab45 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 14} -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {Cell 1} 
    vTcl:DefineAlias "$top.lab45" "Label1" vTcl:WidgetProc "toplevel" 1
    button $top.but46 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command SetTC1 -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text set 
    vTcl:DefineAlias "$top.but46" "SetT1" vTcl:WidgetProc "toplevel" 1
    text $top.tex47 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 74 -wrap word 
    .top42.tex47 configure -font "TkTextFont"
    .top42.tex47 insert end text
    vTcl:DefineAlias "$top.tex47" "Cell1_read" vTcl:WidgetProc "toplevel" 1
    text $top.tex48 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 74 -wrap word 
    .top42.tex48 configure -font "TkTextFont"
    .top42.tex48 insert end text
    vTcl:DefineAlias "$top.tex48" "Cell1_set" vTcl:WidgetProc "toplevel" 1
    label $top.lab49 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {T read} 
    vTcl:DefineAlias "$top.lab49" "Label2" vTcl:WidgetProc "toplevel" 1
    label $top.lab50 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text Setpoint 
    vTcl:DefineAlias "$top.lab50" "Label2_4" vTcl:WidgetProc "toplevel" 1
    label $top.lab51 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {open since:} 
    vTcl:DefineAlias "$top.lab51" "Label2_5" vTcl:WidgetProc "toplevel" 1
    text $top.tex52 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 74 -wrap word 
    .top42.tex52 configure -font "TkTextFont"
    .top42.tex52 insert end text
    vTcl:DefineAlias "$top.tex52" "Cell1_time" vTcl:WidgetProc "toplevel" 1
    label $top.lab53 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 14} -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {Cell 2} 
    vTcl:DefineAlias "$top.lab53" "Label1_7" vTcl:WidgetProc "toplevel" 1
    label $top.lab54 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {T read} 
    vTcl:DefineAlias "$top.lab54" "Label2_8" vTcl:WidgetProc "toplevel" 1
    button $top.but55 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command OpenCell2 -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text Open 
    vTcl:DefineAlias "$top.but55" "open2" vTcl:WidgetProc "toplevel" 1
    button $top.but56 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command CloseCell2 -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text Close 
    vTcl:DefineAlias "$top.but56" "close2" vTcl:WidgetProc "toplevel" 1
    button $top.but57 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command Cell2_o1 -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text 1 
    vTcl:DefineAlias "$top.but57" "Button1_3" vTcl:WidgetProc "toplevel" 1
    button $top.but58 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command Cell2_o1 -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text 2 
    vTcl:DefineAlias "$top.but58" "Button1_4" vTcl:WidgetProc "toplevel" 1
    button $top.but59 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command Cell2_o1 -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text 3 
    vTcl:DefineAlias "$top.but59" "Button1_5" vTcl:WidgetProc "toplevel" 1
    button $top.but60 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command Cell2_o1 -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text 4 
    vTcl:DefineAlias "$top.but60" "Button1_2" vTcl:WidgetProc "toplevel" 1
    button $top.but62 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command Cell2_o1 -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text 1-2 
    vTcl:DefineAlias "$top.but62" "Button1_6" vTcl:WidgetProc "toplevel" 1
    text $top.tex65 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 74 -wrap word 
    .top42.tex65 configure -font "TkTextFont"
    .top42.tex65 insert end text
    vTcl:DefineAlias "$top.tex65" "Cell2_11_read" vTcl:WidgetProc "toplevel" 1
    text $top.tex66 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 74 -wrap word 
    .top42.tex66 configure -font "TkTextFont"
    .top42.tex66 insert end text
    vTcl:DefineAlias "$top.tex66" "Cell2_2_read" vTcl:WidgetProc "toplevel" 1
    text $top.tex67 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 74 -wrap word 
    .top42.tex67 configure -font "TkTextFont"
    .top42.tex67 insert end text
    vTcl:DefineAlias "$top.tex67" "Cell2_3_read" vTcl:WidgetProc "toplevel" 1
    text $top.tex68 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 74 -wrap word 
    .top42.tex68 configure -font "TkTextFont"
    .top42.tex68 insert end text
    vTcl:DefineAlias "$top.tex68" "Cell2_4_read" vTcl:WidgetProc "toplevel" 1
    label $top.lab69 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text Setpoint 
    vTcl:DefineAlias "$top.lab69" "Label2_3" vTcl:WidgetProc "toplevel" 1
    text $top.tex70 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 74 -wrap word 
    .top42.tex70 configure -font "TkTextFont"
    .top42.tex70 insert end text
    vTcl:DefineAlias "$top.tex70" "Cell2_1_set" vTcl:WidgetProc "toplevel" 1
    text $top.tex71 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 74 -wrap word 
    .top42.tex71 configure -font "TkTextFont"
    .top42.tex71 insert end text
    vTcl:DefineAlias "$top.tex71" "Cell2_2_set" vTcl:WidgetProc "toplevel" 1
    text $top.tex72 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 74 -wrap word 
    .top42.tex72 configure -font "TkTextFont"
    .top42.tex72 insert end text
    vTcl:DefineAlias "$top.tex72" "Cell2_3_set" vTcl:WidgetProc "toplevel" 1
    text $top.tex73 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 74 -wrap word 
    .top42.tex73 configure -font "TkTextFont"
    .top42.tex73 insert end text
    vTcl:DefineAlias "$top.tex73" "Cell2_4_set" vTcl:WidgetProc "toplevel" 1
    button $top.but74 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command Cell2_SetT1 -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text set 
    vTcl:DefineAlias "$top.but74" "setT21" vTcl:WidgetProc "toplevel" 1
    button $top.but75 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command Cell2_SetT2 -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text set 
    vTcl:DefineAlias "$top.but75" "setT22" vTcl:WidgetProc "toplevel" 1
    button $top.but76 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command Cell2_SetT3 -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text set 
    vTcl:DefineAlias "$top.but76" "setT2" vTcl:WidgetProc "toplevel" 1
    button $top.but77 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command Cell2_SetT4 -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text set 
    vTcl:DefineAlias "$top.but77" "setT24" vTcl:WidgetProc "toplevel" 1
    label $top.lab78 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {open since:} 
    vTcl:DefineAlias "$top.lab78" "Label2_6" vTcl:WidgetProc "toplevel" 1
    text $top.tex79 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 74 -wrap word 
    .top42.tex79 configure -font "TkTextFont"
    .top42.tex79 insert end text
    vTcl:DefineAlias "$top.tex79" "Text1_8" vTcl:WidgetProc "toplevel" 1
    button $top.but80 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command CallMenu -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text menu 
    vTcl:DefineAlias "$top.but80" "menu" vTcl:WidgetProc "toplevel" 1
    button $top.but81 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command StatusCheck -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text {status check} 
    vTcl:DefineAlias "$top.but81" "statusCheck" vTcl:WidgetProc "toplevel" 1
    text $top.tex82 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 44 -wrap word 
    .top42.tex82 configure -font "TkTextFont"
    .top42.tex82 insert end text
    vTcl:DefineAlias "$top.tex82" "Stepper_status" vTcl:WidgetProc "toplevel" 1
    label $top.lab83 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text Steppers 
    vTcl:DefineAlias "$top.lab83" "Label3" vTcl:WidgetProc "toplevel" 1
    label $top.lab84 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {PID s} 
    vTcl:DefineAlias "$top.lab84" "Label3_5" vTcl:WidgetProc "toplevel" 1
    text $top.tex85 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 44 -wrap word 
    .top42.tex85 configure -font "TkTextFont"
    .top42.tex85 insert end text
    vTcl:DefineAlias "$top.tex85" "PIDs_Status" vTcl:WidgetProc "toplevel" 1
    text $top.tex43 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 264 -wrap word 
    .top42.tex43 configure -font "TkTextFont"
    .top42.tex43 insert end text
    vTcl:DefineAlias "$top.tex43" "ProgramPath" vTcl:WidgetProc "toplevel" 1
    button $top.but45 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command SelectProgram \
        -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text select 
    vTcl:DefineAlias "$top.but45" "selectPath" vTcl:WidgetProc "toplevel" 1
    label $top.lab46 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 14} -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {Growth Program} 
    vTcl:DefineAlias "$top.lab46" "Label1_8" vTcl:WidgetProc "toplevel" 1
    button $top.but47 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command LoadProgram -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text load 
    vTcl:DefineAlias "$top.but47" "loadProgram" vTcl:WidgetProc "toplevel" 1
    vTcl::widgets::ttk::scrolledtext::CreateCmd $top.scr49 \
        -background $vTcl(actual_gui_bg) -height 75 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -width 125 
    vTcl:DefineAlias "$top.scr49" "program_prev" vTcl:WidgetProc "toplevel" 1

    $top.scr49.01 configure -background white \
        -font TkTextFont \
        -foreground black \
        -height 3 \
        -highlightbackground #d9d9d9 \
        -highlightcolor black \
        -insertbackground black \
        -insertborderwidth 3 \
        -selectbackground #c4c4c4 \
        -selectforeground black \
        -width 10 \
        -wrap none
    vTcl::widgets::ttk::scrolledtext::CreateCmd $top.scr50 \
        -background $vTcl(actual_gui_bg) -height 75 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -width 125 
    vTcl:DefineAlias "$top.scr50" "Program_status" vTcl:WidgetProc "toplevel" 1

    $top.scr50.01 configure -background white \
        -font TkTextFont \
        -foreground black \
        -height 3 \
        -highlightbackground #d9d9d9 \
        -highlightcolor black \
        -insertbackground black \
        -insertborderwidth 3 \
        -selectbackground #c4c4c4 \
        -selectforeground black \
        -width 10 \
        -wrap none
    label $top.lab52 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text Program 
    vTcl:DefineAlias "$top.lab52" "Label4" vTcl:WidgetProc "toplevel" 1
    label $top.lab55 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text Status 
    vTcl:DefineAlias "$top.lab55" "Label4_12" vTcl:WidgetProc "toplevel" 1
    button $top.but61 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command RunProgram -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text run 
    vTcl:DefineAlias "$top.but61" "runprogram" vTcl:WidgetProc "toplevel" 1
    button $top.but63 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command PauseProgram -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text pause 
    vTcl:DefineAlias "$top.but63" "pauseProgram" vTcl:WidgetProc "toplevel" 1
    button $top.but64 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command StopProgram -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text STOP 
    vTcl:DefineAlias "$top.but64" "stopProgram" vTcl:WidgetProc "toplevel" 1
    label $top.lab65 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 14} -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text Sample 
    vTcl:DefineAlias "$top.lab65" "Label1_13" vTcl:WidgetProc "toplevel" 1
    label $top.lab66 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {T read} 
    vTcl:DefineAlias "$top.lab66" "Label2_14" vTcl:WidgetProc "toplevel" 1
    text $top.tex69 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 74 -wrap word 
    .top42.tex69 configure -font "TkTextFont"
    .top42.tex69 insert end text
    vTcl:DefineAlias "$top.tex69" "T sample" vTcl:WidgetProc "toplevel" 1
    label $top.lab70 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text Setpoint 
    vTcl:DefineAlias "$top.lab70" "Label2_1" vTcl:WidgetProc "toplevel" 1
    text $top.tex74 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 74 -wrap word 
    .top42.tex74 configure -font "TkTextFont"
    .top42.tex74 insert end text
    vTcl:DefineAlias "$top.tex74" "SampleSetpoint" vTcl:WidgetProc "toplevel" 1
    button $top.but78 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #5b5b5b -command SetTSample -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text set 
    vTcl:DefineAlias "$top.but78" "set_substrateT" vTcl:WidgetProc "toplevel" 1
    label $top.lab79 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {PID 1} 
    vTcl:DefineAlias "$top.lab79" "Label3_4" vTcl:WidgetProc "toplevel" 1
    label $top.lab80 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {PID 2} 
    vTcl:DefineAlias "$top.lab80" "Label3_6" vTcl:WidgetProc "toplevel" 1
    text $top.tex81 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 44 -wrap word 
    .top42.tex81 configure -font "TkTextFont"
    .top42.tex81 insert end text
    vTcl:DefineAlias "$top.tex81" "PID1_Status" vTcl:WidgetProc "toplevel" 1
    text $top.tex83 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 44 -wrap word 
    .top42.tex83 configure -font "TkTextFont"
    .top42.tex83 insert end text
    vTcl:DefineAlias "$top.tex83" "PID2_Status" vTcl:WidgetProc "toplevel" 1
    ttk::separator $top.tSe84
    vTcl:DefineAlias "$top.tSe84" "TSeparator1" vTcl:WidgetProc "toplevel" 1
    ttk::separator $top.tSe85
    vTcl:DefineAlias "$top.tSe85" "TSeparator1_8" vTcl:WidgetProc "toplevel" 1
    ttk::separator $top.tSe86
    vTcl:DefineAlias "$top.tSe86" "TSeparator1_9" vTcl:WidgetProc "toplevel" 1
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.but43 \
        -in $top -x 60 -y 160 -width 67 -relwidth 0 -height 64 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but44 \
        -in $top -x 140 -y 160 -width 67 -height 64 -anchor nw \
        -bordermode ignore 
    place $top.lab45 \
        -in $top -x 10 -y 110 -width 74 -relwidth 0 -height 41 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but46 \
        -in $top -x 230 -y 260 -width 67 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.tex47 \
        -in $top -x 60 -y 260 -width 74 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.tex48 \
        -in $top -x 150 -y 260 -width 74 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.lab49 \
        -in $top -x 60 -y 230 -anchor nw -bordermode ignore 
    place $top.lab50 \
        -in $top -x 150 -y 230 -width 59 -relwidth 0 -height 21 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab51 \
        -in $top -x 50 -y 300 -width 79 -relwidth 0 -height 21 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.tex52 \
        -in $top -x 140 -y 300 -width 74 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.lab53 \
        -in $top -x 20 -y 330 -width 74 -height 41 -anchor nw \
        -bordermode ignore 
    place $top.lab54 \
        -in $top -x 60 -y 490 -width 39 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.but55 \
        -in $top -x 60 -y 370 -width 67 -height 64 -anchor nw \
        -bordermode ignore 
    place $top.but56 \
        -in $top -x 140 -y 370 -width 67 -height 64 -anchor nw \
        -bordermode ignore 
    place $top.but57 \
        -in $top -x 60 -y 440 -width 27 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but58 \
        -in $top -x 90 -y 440 -width 27 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but59 \
        -in $top -x 120 -y 440 -width 27 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.but60 \
        -in $top -x 150 -y 440 -width 27 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.but62 \
        -in $top -x 180 -y 440 -width 27 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex65 \
        -in $top -x 110 -y 490 -width 74 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex66 \
        -in $top -x 110 -y 520 -width 74 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex67 \
        -in $top -x 110 -y 550 -width 74 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex68 \
        -in $top -x 110 -y 580 -width 74 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.lab69 \
        -in $top -x 200 -y 490 -width 59 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.tex70 \
        -in $top -x 260 -y 490 -width 74 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex71 \
        -in $top -x 260 -y 520 -width 74 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex72 \
        -in $top -x 260 -y 550 -width 74 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex73 \
        -in $top -x 260 -y 580 -width 74 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.but74 \
        -in $top -x 350 -y 490 -width 67 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.but75 \
        -in $top -x 350 -y 520 -width 67 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.but76 \
        -in $top -x 350 -y 550 -width 67 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.but77 \
        -in $top -x 350 -y 580 -width 67 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.lab78 \
        -in $top -x 50 -y 620 -width 79 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.tex79 \
        -in $top -x 140 -y 620 -width 74 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.but80 \
        -in $top -x 340 -y 10 -width 107 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but81 \
        -in $top -x 340 -y 40 -width 107 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex82 \
        -in $top -x 400 -y 80 -width 44 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab83 \
        -in $top -x 340 -y 80 -anchor nw -bordermode ignore 
    place $top.lab84 \
        -in $top -x 340 -y 110 -width 51 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.tex85 \
        -in $top -x 400 -y 110 -width 44 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex43 \
        -in $top -x 20 -y 710 -width 264 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but45 \
        -in $top -x 300 -y 710 -width 67 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.lab46 \
        -in $top -x 20 -y 660 -width 154 -relwidth 0 -height 41 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but47 \
        -in $top -x 380 -y 710 -width 67 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.scr49 \
        -in $top -x 70 -y 750 -width 261 -relwidth 0 -height 101 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.scr50 \
        -in $top -x 70 -y 860 -width 261 -height 101 -anchor nw \
        -bordermode ignore 
    place $top.lab52 \
        -in $top -x 10 -y 750 -anchor nw -bordermode ignore 
    place $top.lab55 \
        -in $top -x 10 -y 860 -width 52 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.but61 \
        -in $top -x 350 -y 750 -width 67 -relwidth 0 -height 64 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but63 \
        -in $top -x 350 -y 820 -width 67 -relwidth 0 -height 24 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but64 \
        -in $top -x 350 -y 850 -width 67 -relwidth 0 -height 64 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab65 \
        -in $top -x 10 -y 10 -width 74 -height 41 -anchor nw \
        -bordermode ignore 
    place $top.lab66 \
        -in $top -x 50 -y 50 -width 39 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.tex69 \
        -in $top -x 50 -y 70 -width 74 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.lab70 \
        -in $top -x 140 -y 50 -width 59 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.tex74 \
        -in $top -x 140 -y 70 -width 74 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.but78 \
        -in $top -x 220 -y 70 -width 67 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.lab79 \
        -in $top -x 340 -y 140 -width 51 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.lab80 \
        -in $top -x 340 -y 170 -width 51 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.tex81 \
        -in $top -x 400 -y 140 -width 44 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tex83 \
        -in $top -x 400 -y 170 -width 44 -height 24 -anchor nw \
        -bordermode ignore 
    place $top.tSe84 \
        -in $top -x 20 -y 660 -width 420 -anchor nw -bordermode inside 
    place $top.tSe85 \
        -in $top -x 20 -y 330 -width 420 -height 2 -anchor nw \
        -bordermode ignore 
    place $top.tSe86 \
        -in $top -x 20 -y 110 -width 290 -height 2 -anchor nw \
        -bordermode ignore 

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

