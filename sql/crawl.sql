-- MySQL dump 10.13  Distrib 5.6.25, for Linux (i686)
--
-- Host: localhost    Database: cms2
-- ------------------------------------------------------
-- Server version	5.6.25

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cw_cat_relat`
--

DROP TABLE IF EXISTS `cw_cat_relat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cw_cat_relat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lcid` int(11) NOT NULL,
  `rcid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lcid` (`lcid`,`rcid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cw_cat_relat`
--

LOCK TABLES `cw_cat_relat` WRITE;
/*!40000 ALTER TABLE `cw_cat_relat` DISABLE KEYS */;
/*!40000 ALTER TABLE `cw_cat_relat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cw_categories`
--

DROP TABLE IF EXISTS `cw_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cw_categories` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `cname` varchar(100) NOT NULL,
  `sid` int(11) NOT NULL,
  `url` varchar(100) NOT NULL,
  `pcnt` int(11) NOT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cw_categories`
--

LOCK TABLES `cw_categories` WRITE;
/*!40000 ALTER TABLE `cw_categories` DISABLE KEYS */;
INSERT INTO `cw_categories` VALUES (1,'段子',1,'/skl/index_%s.htm',96);
/*!40000 ALTER TABLE `cw_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cw_options`
--

DROP TABLE IF EXISTS `cw_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cw_options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `okey` varchar(100) NOT NULL,
  `ovalue` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `okey` (`okey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cw_options`
--

LOCK TABLES `cw_options` WRITE;
/*!40000 ALTER TABLE `cw_options` DISABLE KEYS */;
/*!40000 ALTER TABLE `cw_options` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cw_posts`
--

DROP TABLE IF EXISTS `cw_posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cw_posts` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) NOT NULL DEFAULT '0',
  `url` varchar(255) NOT NULL DEFAULT '',
  `title` varchar(150) NOT NULL DEFAULT '',
  `keywords` varchar(255) NOT NULL DEFAULT '',
  `description` varchar(255) NOT NULL DEFAULT '',
  `content` mediumtext NOT NULL,
  `uid` int(11) NOT NULL DEFAULT '0',
  `addtime` int(11) NOT NULL DEFAULT '0',
  `pubtime` int(11) NOT NULL DEFAULT '0',
  `synctime` int(11) NOT NULL DEFAULT '0',
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `ext` text NOT NULL,
  PRIMARY KEY (`pid`),
  UNIQUE KEY `cid` (`cid`,`url`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cw_posts`
--

LOCK TABLES `cw_posts` WRITE;
/*!40000 ALTER TABLE `cw_posts` DISABLE KEYS */;
/*!40000 ALTER TABLE `cw_posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cw_sites`
--

DROP TABLE IF EXISTS `cw_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cw_sites` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `sname` varchar(100) NOT NULL,
  `host` varchar(100) NOT NULL,
  `stype` varchar(100) NOT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cw_sites`
--

LOCK TABLES `cw_sites` WRITE;
/*!40000 ALTER TABLE `cw_sites` DISABLE KEYS */;
INSERT INTO `cw_sites` VALUES (1,'haha365','www.haha365.com','unknown'),(2,'pouman','www.pouman.com','dedecms');
/*!40000 ALTER TABLE `cw_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cw_users`
--

DROP TABLE IF EXISTS `cw_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cw_users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `uname` varchar(100) NOT NULL,
  `addtime` int(11) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cw_users`
--

LOCK TABLES `cw_users` WRITE;
/*!40000 ALTER TABLE `cw_users` DISABLE KEYS */;
INSERT INTO `cw_users` VALUES (1,'admin',0);
/*!40000 ALTER TABLE `cw_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-10-05 12:17:02
