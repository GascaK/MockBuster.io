scrollID=0;
vPos=0;

function onWard() {
    vPos+=2;
    window.scroll(0,vPos);
    vPos%=1000;
    scrollID=setTimeout("onWard()",40);
}