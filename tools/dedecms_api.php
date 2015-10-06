<?php
/*
	[LocoySpider] (C)2005-2010 Lewell Inc.
	火车采集器 DedeCMS 5.6 UTF8 文章发布接口
	最后更新:2010.07.10 by RQ204
	视频教程:http://video.locoy.com/jiekou/dede/dede56_article.7z
*/

/********密码验证***********/
$password='admin';				                   //这个密码是登陆验证用的.您需要在模块里设置和这里一样的密码....注意一定需要修改.
if($password!=$_REQUEST['password']) {  //安全检测,密码不符则退出
	ret('验证密码错误', -1);
}


/****以下代码非专业人员不建议修改***************/
if($_POST) $ispost=true;
//require_once(dirname(__FILE__).'/config.php');
define('DEDEADMIN', ereg_replace("[/\\]{1,}", '/', dirname(__FILE__) ) );
require_once(DEDEADMIN.'/../include/common.inc.php');
require_once(DEDEINC.'/userlogin.class.php');
header('Cache-Control:private');
$dsql->safeCheck = false;
$dsql->SetLongLink();

//获得当前脚本名称，如果你的系统被禁用了$_SERVER变量，请自行更改这个选项
$dedeNowurl = $s_scriptName = '';
$isUrlOpen = @ini_get('allow_url_fopen');
$dedeNowurl = GetCurUrl();
$dedeNowurls = explode('?', $dedeNowurl);
$s_scriptName = $dedeNowurls[0];
$cfg_remote_site = empty($cfg_remote_site)? 'N' : $cfg_remote_site;
	
//启用远程站点则创建FTP类
if($cfg_remote_site=='Y')
{
	require_once(DEDEINC.'/ftp.class.php');
	if(file_exists(DEDEDATA."/cache/inc_remote_config.php"))
	{
		require_once DEDEDATA."/cache/inc_remote_config.php";
	}
	if(empty($remoteuploads)) $remoteuploads = 0;
	if(empty($remoteupUrl)) $remoteupUrl = '';
	$config = array(
	  'hostname' => $GLOBALS['cfg_ftp_host'],
	  'username' => $GLOBALS['cfg_ftp_user'],
	  'password' => $GLOBALS['cfg_ftp_pwd'],
	  'debug' => 'TRUE'
	);
	$ftp = new FTP($config); 

	//初始化FTP配置
	if($remoteuploads==1){
		$ftpconfig = array(
			'hostname'=>$rmhost, 
			'port'=>$rmport,
			'username'=>$rmname,
			'password'=>$rmpwd
		);
	}
}

function UpDateMemberModCache()
{
	global $dsql;
	$cachefile = DEDEDATA.'/cache/member_model.inc';

	$dsql->SetQuery("SELECT * FROM `#@__member_model` WHERE state='1'");
	$dsql->Execute();
	$fp1 = fopen($cachefile,'w');
	$phph = '?';
	$fp1Header = "<{$phph}php\r\nglobal \$_MemberMod;\r\n\$_MemberMod=array();\r\n";
	fwrite($fp1,$fp1Header);
	while($row=$dsql->GetObject())
	{
		fwrite($fp1,"\$_MemberMod[{$row->id}]=array('{$row->name}','{$row->table}');\r\n");
	}
	fwrite($fp1,"{$phph}>");
	fclose($fp1);
}


function DedeInclude($filename,$isabs=false)
{
	return $isabs ? $filename : DEDEADMIN.'/'.$filename;
}

//config引用结束

//CheckPurview('a_New,a_AccNew');
require_once(DEDEINC.'/customfields.func.php');
require_once(DEDEADMIN.'/inc/inc_archives_functions.php');
if(file_exists(DEDEDATA.'/template.rand.php'))
{
	require_once(DEDEDATA.'/template.rand.php');
}

$dsql->SetSql("Select id as cid,reid as pid,typename as cname,ispart,topid  from `#@__arctype` where channeltype =1 order by sortrank");
$dsql->Execute();
while($row=$dsql->GetObject())
{
	$cates[]=array('cid'=>$row->cid,'pid'=>$row->pid,'cname'=>$row->cname,'ispart'=>$row->ispart,'topid'=>$row->topid);
}

if(!$ispost)
{
	echo "<select name='list'>";
	echo maketree($cates,0,'');
	echo '</select>';
	exit();
}

/*--------------------------------
function __save(){  }
-------------------------------*/
else
{
	require_once(DEDEINC.'/image.func.php');
	require_once(DEDEINC.'/oxwindow.class.php');
	//检验用户登录状态
	$userinfo=$dsql->GetOne("Select * from `#@__member` where userid='$username'");
	if(!$userinfo) {
		ret("不存在用户$username", -100);
	}
	$uid=$userinfo['mid'];
	//检测栏目信息
	foreach ($cates as $f=>$v)
	{
		if($v['cid']==$typeid)
		{		
			$eid=$v;
			if($v['ispart']!=0) {
				
			}
		}
	}
	if (!$eid) {
		ret("不存在的栏目id:$typeid", -2);
	}

	require_once(DEDEINC.'/image.func.php');
	//require_once(DEDEINC.'/oxwindow.class.php');
	$flag = isset($flags) ? join(',',$flags) : '';
	$notpost = isset($notpost) && $notpost == 1 ? 1: 0;
	
	if(empty($typeid2)) $typeid2 = '';
	if(!isset($autokey)) $autokey = 0;
	if(!isset($remote)) $remote = 0;
	if(!isset($dellink)) $dellink = 0;
	if(!isset($autolitpic)) $autolitpic = 0;
	if(empty($click)) $click = ($cfg_arc_click=='-1' ? mt_rand(50, 200) : $cfg_arc_click);
	if(empty($typeid)) {
		ret("请指定文档的栏目！", -3);
	}
	if(empty($channelid)) {
		ret("文档为非指定的类型，请检查你发布内容的表单是否合法！", -4);
	}
	if(!CheckChannel($typeid,$channelid)) {
		ret("你所选择的栏目与当前模型不相符，请选择白色的选项！", -5);
	}

	//对保存的内容进行处理
	if(empty($writer))$writer=$username;
	if(empty($source))$source='未知';
	$pubdate = GetMkTime($pubdate);
	if(!$pubdate) $pubdate=time();
	$senddate = time();
	$sortrank = AddDay($pubdate,$sortup);
	$ismake = $ishtml==0 ? -1 : 0;
	$title = ereg_replace('"', '＂', $title);
	$title = htmlspecialchars(cn_substrR($title,$cfg_title_maxlen));
	$shorttitle = cn_substrR($shorttitle,36);
	$color =  cn_substrR($color,7);
	$writer =  cn_substrR($writer,20);
	$source = cn_substrR($source,30);
	$description = cn_substrR($description,$cfg_auot_description);
	$keywords = cn_substrR($keywords,60);
	$filename = trim(cn_substrR($filename,40));
	$userip = GetIP();
	$isremote  = (empty($isremote)? 0  : $isremote);
	$serviterm=empty($serviterm)? "" : $serviterm;

	// if(!TestPurview('a_Check,a_AccCheck,a_MyCheck'))
	// {
		// $arcrank = -1;
	// }
	$adminid = $uid;

	//处理上传的缩略图
	if(empty($ddisremote))
	{
		$ddisremote = 0;
	}
	
	$litpic = GetDDImage('none', $picname, $ddisremote);

	//生成文档ID
	$arcID = GetIndexKey($arcrank,$typeid,$sortrank,$channelid,$senddate,$adminid);
    
	if(empty($arcID)) {
		ret("无法获得主键，因此无法进行后续操作！", -6);
	}
	if(trim($title) == '') {
		ret('标题不能为空', -7);
	}

	//处理body字段自动摘要、自动提取缩略图等
	$body = AnalyseHtmlBody($body,$description,$litpic,$keywords,'htmltext');

	//自动分页
	if($sptype=='auto')
	{
		$body = SpLongBody($body,$spsize*1024,"#p#分页标题#e#");
	}

	//分析处理附加表数据
	$inadd_f = $inadd_v = '';
	if(!empty($dede_addonfields))
	{
		$addonfields = explode(';',$dede_addonfields);
		if(is_array($addonfields))
		{
			foreach($addonfields as $v)
			{
				if($v=='') continue;
				$vs = explode(',',$v);
				if($vs[1]=='htmltext'||$vs[1]=='textdata')
				{
					${$vs[0]} = AnalyseHtmlBody(${$vs[0]},$description,$litpic,$keywords,$vs[1]);
				}
				else
				{
					if(!isset(${$vs[0]})) ${$vs[0]} = '';
					${$vs[0]} = GetFieldValueA(${$vs[0]},$vs[1],$arcID);
				}
				$inadd_f .= ','.$vs[0];
				$inadd_v .= " ,'".${$vs[0]}."' ";
			}
		}
	}

	//处理图片文档的自定义属性
	if($litpic!='' && !ereg('p',$flag))
	{
		$flag = ($flag=='' ? 'p' : $flag.',p');
	}
	if($redirecturl!='' && !ereg('j',$flag))
	{
		$flag = ($flag=='' ? 'j' : $flag.',j');
	}
	
	//跳转网址的文档强制为动态
	if(ereg('j', $flag)) $ismake = -1;

	//保存到主表
	$query = "INSERT INTO `#@__archives`(id,typeid,typeid2,sortrank,flag,ismake,channel,arcrank,click,money,title,shorttitle,
    color,writer,source,litpic,pubdate,senddate,mid,notpost,description,keywords,filename,dutyadmin,weight)
    VALUES ('$arcID','$typeid','$typeid2','$sortrank','$flag','$ismake','$channelid','$arcrank','$click','$money',
    '$title','$shorttitle','$color','$writer','$source','$litpic','$pubdate','$senddate',
    '$adminid','$notpost','$description','$keywords','$filename','$adminid','$weight');";

	if(!$dsql->ExecuteNoneQuery($query)) {
		$gerr = $dsql->GetError();
		$dsql->ExecuteNoneQuery("Delete From `#@__arctiny` where id='$arcID'");
		ret("把数据保存到数据库主表 `#@__archives` 时出错，请把相关信息提交给DedeCms官方。", -9);
	}

	//保存到附加表
	$cts = $dsql->GetOne("Select addtable From `#@__channeltype` where id='$channelid' ");
	$addtable = trim($cts['addtable']);
	if(empty($addtable))
	{
		$dsql->ExecuteNoneQuery("Delete From `#@__archives` where id='$arcID'");
		$dsql->ExecuteNoneQuery("Delete From `#@__arctiny` where id='$arcID'");
		ret("没找到当前模型[{$channelid}]的主表信息，无法完成操作！。", -10);
	}
	$useip = GetIP();
	$templet = empty($templet) ? '' : $templet;
	$query = "INSERT INTO `{$addtable}`(aid,typeid,redirecturl,templet,userip,body{$inadd_f}) Values('$arcID','$typeid','$redirecturl','$templet','$useip','$body'{$inadd_v})";
	if(!$dsql->ExecuteNoneQuery($query))
	{
		$gerr = $dsql->GetError();
		$dsql->ExecuteNoneQuery("Delete From `#@__archives` where id='$arcID'");
		$dsql->ExecuteNoneQuery("Delete From `#@__arctiny` where id='$arcID'");
		ret("把数据保存到数据库附加表 `{$addtable}` 时出错，请把相关信息提交给DedeCms官方。", -11);
	}

	//生成HTML
	InsertTags($tags,$arcID);
	if($cfg_remote_site=='Y' && $isremote=="1")
	{	
		if($serviterm!=""){
			list($servurl,$servuser,$servpwd) = explode(',',$serviterm);
			$config=array( 'hostname' => $servurl, 'username' => $servuser, 'password' => $servpwd,'debug' => 'TRUE');
		}else{
			$config=array();
		}
		if(!$ftp->connect($config)) exit('Error:None FTP Connection!');
	}
	$artUrl = MakeArt($arcID,true,true,$isremote);
	if($artUrl=='')
	{
		$artUrl = $cfg_phpurl."/view.php?aid=$arcID";
	}
	ClearMyAddon($arcID, $title);
	//返回成功信息
	// $msg = "    　　请选择你的后续操作：
 //    <a href='article_add.php?cid=$typeid'><u>继续发布文章</u></a>
 //    &nbsp;&nbsp;
 //    <a href='$artUrl' target='_blank'><u>查看文章</u></a>
 //    &nbsp;&nbsp;
 //    <a href='archives_do.php?aid=".$arcID."&dopost=editArchives'><u>更改文章</u></a>
 //    &nbsp;&nbsp;
 //    <a href='catalog_do.php?cid=$typeid&dopost=listArchives'><u>已发布文章管理</u></a>
 //    &nbsp;&nbsp;
 //    $backurl
 //  ";
 //  $msg = "<div style=\"line-height:36px;height:36px\">{$msg}</div>".GetUpdateTest();
	// $wintitle = "成功发布文章！";
	// $wecome_info = "文章管理::发布文章";
	// $win = new OxWindow();
	// $win->AddTitle("成功发布文章：");
	// $win->AddMsgItem($msg);
	// $winform = $win->GetWindow("hand","&nbsp;",false);
	// $win->Display();
	ret("成功发布文章！");
}
/***生成目录的一个遍历算法***/
function maketree($ar,$id,$pre)
{
	$ids='';
	foreach($ar as $k=>$v){
		$pid=$v['pid'];
		$cname=$v['cname'];
		$cid=$v['cid'];
		if($pid==$id)
		{
			$ids.="<option value='$cid'>{$pre}{$cname}</option>";
			foreach($ar as $kk=>$vv)
			{
				$pp=$vv['pid'];
				if($pp==$cid)
				{ 
					$ids.=maketree($ar,$cid,$pre."&nbsp;&nbsp;");
					break;
				}
			}
		}
	}
	return $ids;
}

function ret($msg, $code = 0) {
	$arr = array('ret'=>$code, 'msg'=>$msg);
	die(json_encode($arr));
}
?>