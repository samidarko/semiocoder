-- MySQL dump 10.13  Distrib 5.5.24, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: semiocoder
-- ------------------------------------------------------
-- Server version	5.5.24-0ubuntu0.12.04.1

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_9af0b65a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add message',4,'add_message'),(11,'Can change message',4,'change_message'),(12,'Can delete message',4,'delete_message'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add site',7,'add_site'),(20,'Can change site',7,'change_site'),(21,'Can delete site',7,'delete_site'),(22,'Can add log entry',8,'add_logentry'),(23,'Can change log entry',8,'change_logentry'),(24,'Can delete log entry',8,'delete_logentry'),(25,'Can add encoder',9,'add_encoder'),(26,'Can change encoder',9,'change_encoder'),(27,'Can delete encoder',9,'delete_encoder'),(28,'Can add extension',10,'add_extension'),(29,'Can change extension',10,'change_extension'),(30,'Can delete extension',10,'delete_extension'),(31,'Can add job',11,'add_job'),(32,'Can change job',11,'change_job'),(33,'Can delete job',11,'delete_job'),(34,'Can add joblist',12,'add_joblist'),(35,'Can change joblist',12,'change_joblist'),(36,'Can delete joblist',12,'delete_joblist'),(37,'Can add task',13,'add_task'),(38,'Can change task',13,'change_task'),(39,'Can delete task',13,'delete_task'),(40,'Can add task history',14,'add_taskhistory'),(41,'Can change task history',14,'change_taskhistory'),(42,'Can delete task history',14,'delete_taskhistory'),(43,'Can add task state',15,'add_taskmeta'),(44,'Can change task state',15,'change_taskmeta'),(45,'Can delete task state',15,'delete_taskmeta'),(46,'Can add saved group result',16,'add_tasksetmeta'),(47,'Can change saved group result',16,'change_tasksetmeta'),(48,'Can delete saved group result',16,'delete_tasksetmeta'),(49,'Can add interval',17,'add_intervalschedule'),(50,'Can change interval',17,'change_intervalschedule'),(51,'Can delete interval',17,'delete_intervalschedule'),(52,'Can add crontab',18,'add_crontabschedule'),(53,'Can change crontab',18,'change_crontabschedule'),(54,'Can delete crontab',18,'delete_crontabschedule'),(55,'Can add periodic tasks',19,'add_periodictasks'),(56,'Can change periodic tasks',19,'change_periodictasks'),(57,'Can delete periodic tasks',19,'delete_periodictasks'),(58,'Can add periodic task',20,'add_periodictask'),(59,'Can change periodic task',20,'change_periodictask'),(60,'Can delete periodic task',20,'delete_periodictask'),(61,'Can add worker',21,'add_workerstate'),(62,'Can change worker',21,'change_workerstate'),(63,'Can delete worker',21,'delete_workerstate'),(64,'Can add task',22,'add_taskstate'),(65,'Can change task',22,'change_taskstate'),(66,'Can delete task',22,'delete_taskstate');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'samidarko','','','samidarko@gmail.com','sha1$71bc7$5a5efd0133d3966908b27fbdabde5b41c3de7505',1,1,1,'2012-08-05 10:00:20','2012-08-04 22:43:38');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`),
  CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celery_taskmeta`
--

DROP TABLE IF EXISTS `celery_taskmeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `celery_taskmeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `result` longtext,
  `date_done` datetime NOT NULL,
  `traceback` longtext,
  `hidden` tinyint(1) NOT NULL,
  `meta` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `celery_taskmeta_c91f1bf` (`hidden`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celery_taskmeta`
--

LOCK TABLES `celery_taskmeta` WRITE;
/*!40000 ALTER TABLE `celery_taskmeta` DISABLE KEYS */;
INSERT INTO `celery_taskmeta` VALUES (1,'e32c2cc4-ad4f-4b41-abb5-8562465c6c0a','SUCCESS','gAJVD2NvZGUgcmV0b3VyIDogMHEBLg==','2012-08-11 23:05:00',NULL,0,'eJxrYKotZAzlSM7IzEkpSs0rZIotZC7WAwBREgb9'),(2,'fd22c7b7-a3ad-4d85-a5fc-fc9047a6cc9f','SUCCESS','gAJVD2NvZGUgcmV0b3VyIDogMHEBLg==','2012-08-12 09:28:00',NULL,0,'eJxrYKotZAzlSM7IzEkpSs0rZIotZC7WAwBREgb9'),(3,'8a1979c4-31d8-4aad-8076-589b662b341b','SUCCESS','gAJVD2NvZGUgcmV0b3VyIDogMHEBLg==','2012-08-12 21:15:01',NULL,0,'eJxrYKotZAzlSM7IzEkpSs0rZIotZC7WAwBREgb9');
/*!40000 ALTER TABLE `celery_taskmeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celery_tasksetmeta`
--

DROP TABLE IF EXISTS `celery_tasksetmeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `celery_tasksetmeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskset_id` varchar(255) NOT NULL,
  `result` longtext NOT NULL,
  `date_done` datetime NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `taskset_id` (`taskset_id`),
  KEY `celery_tasksetmeta_c91f1bf` (`hidden`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celery_tasksetmeta`
--

LOCK TABLES `celery_tasksetmeta` WRITE;
/*!40000 ALTER TABLE `celery_tasksetmeta` DISABLE KEYS */;
/*!40000 ALTER TABLE `celery_tasksetmeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_fbfc09f1` (`user_id`),
  KEY `django_admin_log_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2012-08-05 10:01:41',1,9,'1','encoder: ffmpeg',1,''),(2,'2012-08-05 10:01:58',1,10,'1','.avi',1,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'message','auth','message'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'site','sites','site'),(8,'log entry','admin','logentry'),(9,'encoder','encoder','encoder'),(10,'extension','encoder','extension'),(11,'job','encoder','job'),(12,'joblist','encoder','joblist'),(13,'task','encoder','task'),(14,'task history','encoder','taskhistory'),(15,'task state','djcelery','taskmeta'),(16,'saved group result','djcelery','tasksetmeta'),(17,'interval','djcelery','intervalschedule'),(18,'crontab','djcelery','crontabschedule'),(19,'periodic tasks','djcelery','periodictasks'),(20,'periodic task','djcelery','periodictask'),(21,'worker','djcelery','workerstate'),(22,'task','djcelery','taskstate');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_c25c2c28` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('476341c5bb3fa377917fa455c9a998ba','NWI4YWE4ZmU1MDliMWE2OGI3YjllZGEyMDFkMWY4ZTYyYmIyMjI1YTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2012-08-19 10:00:20'),('5fcdc9972cd416709f2fa4ed16a07add','NWI4YWE4ZmU1MDliMWE2OGI3YjllZGEyMDFkMWY4ZTYyYmIyMjI1YTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2012-08-18 22:44:12');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_crontabschedule`
--

DROP TABLE IF EXISTS `djcelery_crontabschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_crontabschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `minute` varchar(64) NOT NULL,
  `hour` varchar(64) NOT NULL,
  `day_of_week` varchar(64) NOT NULL,
  `day_of_month` varchar(64) NOT NULL,
  `month_of_year` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_crontabschedule`
--

LOCK TABLES `djcelery_crontabschedule` WRITE;
/*!40000 ALTER TABLE `djcelery_crontabschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_crontabschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_intervalschedule`
--

DROP TABLE IF EXISTS `djcelery_intervalschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_intervalschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `every` int(11) NOT NULL,
  `period` varchar(24) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_intervalschedule`
--

LOCK TABLES `djcelery_intervalschedule` WRITE;
/*!40000 ALTER TABLE `djcelery_intervalschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_intervalschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_periodictask`
--

DROP TABLE IF EXISTS `djcelery_periodictask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_periodictask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `task` varchar(200) NOT NULL,
  `interval_id` int(11) DEFAULT NULL,
  `crontab_id` int(11) DEFAULT NULL,
  `args` longtext NOT NULL,
  `kwargs` longtext NOT NULL,
  `queue` varchar(200) DEFAULT NULL,
  `exchange` varchar(200) DEFAULT NULL,
  `routing_key` varchar(200) DEFAULT NULL,
  `expires` datetime DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime DEFAULT NULL,
  `total_run_count` int(10) unsigned NOT NULL,
  `date_changed` datetime NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `djcelery_periodictask_17d2d99d` (`interval_id`),
  KEY `djcelery_periodictask_7aa5fda` (`crontab_id`),
  CONSTRAINT `crontab_id_refs_id_ebff5e74` FOREIGN KEY (`crontab_id`) REFERENCES `djcelery_crontabschedule` (`id`),
  CONSTRAINT `interval_id_refs_id_f2054349` FOREIGN KEY (`interval_id`) REFERENCES `djcelery_intervalschedule` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_periodictask`
--

LOCK TABLES `djcelery_periodictask` WRITE;
/*!40000 ALTER TABLE `djcelery_periodictask` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_periodictask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_periodictasks`
--

DROP TABLE IF EXISTS `djcelery_periodictasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_periodictasks` (
  `ident` smallint(6) NOT NULL,
  `last_update` datetime NOT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_periodictasks`
--

LOCK TABLES `djcelery_periodictasks` WRITE;
/*!40000 ALTER TABLE `djcelery_periodictasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_periodictasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_taskstate`
--

DROP TABLE IF EXISTS `djcelery_taskstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_taskstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(64) NOT NULL,
  `task_id` varchar(36) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `tstamp` datetime NOT NULL,
  `args` longtext,
  `kwargs` longtext,
  `eta` datetime DEFAULT NULL,
  `expires` datetime DEFAULT NULL,
  `result` longtext,
  `traceback` longtext,
  `runtime` double DEFAULT NULL,
  `retries` int(11) NOT NULL,
  `worker_id` int(11) DEFAULT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `djcelery_taskstate_355bfc27` (`state`),
  KEY `djcelery_taskstate_52094d6e` (`name`),
  KEY `djcelery_taskstate_f0ba6500` (`tstamp`),
  KEY `djcelery_taskstate_20fc5b84` (`worker_id`),
  KEY `djcelery_taskstate_c91f1bf` (`hidden`),
  CONSTRAINT `worker_id_refs_id_4e3453a` FOREIGN KEY (`worker_id`) REFERENCES `djcelery_workerstate` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_taskstate`
--

LOCK TABLES `djcelery_taskstate` WRITE;
/*!40000 ALTER TABLE `djcelery_taskstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_taskstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_workerstate`
--

DROP TABLE IF EXISTS `djcelery_workerstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_workerstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(255) NOT NULL,
  `last_heartbeat` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hostname` (`hostname`),
  KEY `djcelery_workerstate_eb8ac7e4` (`last_heartbeat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_workerstate`
--

LOCK TABLES `djcelery_workerstate` WRITE;
/*!40000 ALTER TABLE `djcelery_workerstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_workerstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `encoder_encoder`
--

DROP TABLE IF EXISTS `encoder_encoder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `encoder_encoder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  `path` varchar(100) NOT NULL,
  `inputflag` varchar(10) DEFAULT NULL,
  `outputflag` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `encoder_encoder`
--

LOCK TABLES `encoder_encoder` WRITE;
/*!40000 ALTER TABLE `encoder_encoder` DISABLE KEYS */;
INSERT INTO `encoder_encoder` VALUES (1,'ffmpeg','static/exe/ffmpeg','-i','');
/*!40000 ALTER TABLE `encoder_encoder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `encoder_extension`
--

DROP TABLE IF EXISTS `encoder_extension`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `encoder_extension` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `encoder_extension`
--

LOCK TABLES `encoder_extension` WRITE;
/*!40000 ALTER TABLE `encoder_extension` DISABLE KEYS */;
INSERT INTO `encoder_extension` VALUES (1,'avi');
/*!40000 ALTER TABLE `encoder_extension` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `encoder_job`
--

DROP TABLE IF EXISTS `encoder_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `encoder_job` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `created_by_id` int(11) NOT NULL,
  `created_on` datetime NOT NULL,
  `modified_on` datetime NOT NULL,
  `encoder_id` int(11) NOT NULL,
  `options` varchar(240) NOT NULL,
  `extension_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `encoder_job_b5de30be` (`created_by_id`),
  KEY `encoder_job_cb26579f` (`encoder_id`),
  KEY `encoder_job_cf1302e2` (`extension_id`),
  CONSTRAINT `created_by_id_refs_id_1a23ce97` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `encoder_id_refs_id_dd5d0962` FOREIGN KEY (`encoder_id`) REFERENCES `encoder_encoder` (`id`),
  CONSTRAINT `extension_id_refs_id_788e0313` FOREIGN KEY (`extension_id`) REFERENCES `encoder_extension` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `encoder_job`
--

LOCK TABLES `encoder_job` WRITE;
/*!40000 ALTER TABLE `encoder_job` DISABLE KEYS */;
INSERT INTO `encoder_job` VALUES (1,'job1','',1,'2012-08-05 10:03:15','2012-08-05 10:21:22',1,' -strict experimental -b 300 -s 320x240  -ab 32 -ar 24000 -acodec aac ',1),(3,'qsdfqsdf','',1,'2012-08-12 21:00:28','2012-08-12 21:00:28',1,'-strict experimental -b 300 -s 320x240 -ab 32 -ar 24000 -acodec aac',1);
/*!40000 ALTER TABLE `encoder_job` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `encoder_joblist`
--

DROP TABLE IF EXISTS `encoder_joblist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `encoder_joblist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `created_by_id` int(11) NOT NULL,
  `created_on` datetime NOT NULL,
  `modified_on` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `encoder_joblist_b5de30be` (`created_by_id`),
  CONSTRAINT `created_by_id_refs_id_19488153` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `encoder_joblist`
--

LOCK TABLES `encoder_joblist` WRITE;
/*!40000 ALTER TABLE `encoder_joblist` DISABLE KEYS */;
INSERT INTO `encoder_joblist` VALUES (1,'joblist','',1,'2012-08-05 10:03:50','2012-08-05 10:03:50'),(2,'sdfgsdfg','',1,'2012-08-12 20:59:47','2012-08-12 21:00:47');
/*!40000 ALTER TABLE `encoder_joblist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `encoder_joblist_job`
--

DROP TABLE IF EXISTS `encoder_joblist_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `encoder_joblist_job` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `joblist_id` int(11) NOT NULL,
  `job_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `joblist_id` (`joblist_id`,`job_id`),
  KEY `encoder_joblist_job_9285e896` (`joblist_id`),
  KEY `encoder_joblist_job_751f44ae` (`job_id`),
  CONSTRAINT `joblist_id_refs_id_deb7dff3` FOREIGN KEY (`joblist_id`) REFERENCES `encoder_joblist` (`id`),
  CONSTRAINT `job_id_refs_id_64099867` FOREIGN KEY (`job_id`) REFERENCES `encoder_job` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `encoder_joblist_job`
--

LOCK TABLES `encoder_joblist_job` WRITE;
/*!40000 ALTER TABLE `encoder_joblist_job` DISABLE KEYS */;
INSERT INTO `encoder_joblist_job` VALUES (1,1,1),(4,2,1),(5,2,3);
/*!40000 ALTER TABLE `encoder_joblist_job` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `encoder_task`
--

DROP TABLE IF EXISTS `encoder_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `encoder_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `joblist_id` int(11) NOT NULL,
  `schedule` datetime NOT NULL,
  `owner_id` int(11) NOT NULL,
  `state` varchar(1) NOT NULL,
  `source_file` varchar(100) NOT NULL,
  `notify` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `encoder_task_9285e896` (`joblist_id`),
  KEY `encoder_task_5d52dd10` (`owner_id`),
  CONSTRAINT `joblist_id_refs_id_4afd29a2` FOREIGN KEY (`joblist_id`) REFERENCES `encoder_joblist` (`id`),
  CONSTRAINT `owner_id_refs_id_a4adf6f0` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `encoder_task`
--

LOCK TABLES `encoder_task` WRITE;
/*!40000 ALTER TABLE `encoder_task` DISABLE KEYS */;
/*!40000 ALTER TABLE `encoder_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `encoder_taskhistory`
--

DROP TABLE IF EXISTS `encoder_taskhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `encoder_taskhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `joblist` varchar(30) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `state` varchar(10) NOT NULL,
  `starttime` datetime NOT NULL,
  `endtime` datetime NOT NULL,
  `outputdir` varchar(20) NOT NULL,
  `log` longtext,
  PRIMARY KEY (`id`),
  KEY `encoder_taskhistory_5d52dd10` (`owner_id`),
  CONSTRAINT `owner_id_refs_id_525764d1` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `encoder_taskhistory`
--

LOCK TABLES `encoder_taskhistory` WRITE;
/*!40000 ALTER TABLE `encoder_taskhistory` DISABLE KEYS */;
INSERT INTO `encoder_taskhistory` VALUES (2,'joblist',1,'C','2012-08-12 09:27:59','2012-08-12 09:28:00','','===== Log job1 =============================\n\n<br>Error log :<br>ffmpeg version 0.8.3-4:0.8.3-0ubuntu0.12.04.1, Copyright (c) 2000-2012 the Libav developers\n  built on Jun 12 2012 16:52:09 with gcc 4.6.3\n*** THIS PROGRAM IS DEPRECATED ***\nThis program is only provided for compatibility and will be removed in a future release. Please use avconv instead.\n\nSeems stream 1 codec frame rate differs from container frame rate: 1200.00 (1200/1) -> 30.00 (30/1)\nInput #0, mov,mp4,m4a,3gp,3g2,mj2, from \'media/videos/20120812_092359/IMG_4718.MOV\':\n  Metadata:\n    major_brand     : qt  \n    minor_version   : 0\n    compatible_brands: qt  \n    creation_time   : 2012-08-05 08:15:54\n    encoder         : 5.1.1\n    encoder-fra     : 5.1.1\n    date            : 2012-08-05T10:15:35+0200\n    date-fra        : 2012-08-05T10:15:35+0200\n  Duration: 00:00:10.80, start: 0.000000, bitrate: 807 kb/s\n    Stream #0.0(und): Audio: aac, 44100 Hz, mono, s16, 62 kb/s\n    Metadata:\n      creation_time   : 2012-08-05 08:15:54\n    Stream #0.1(und): Video: h264 (Main), yuv420p, 480x272, 740 kb/s, 30 fps, 30 tbr, 600 tbn, 1200 tbc\n    Metadata:\n      creation_time   : 2012-08-05 08:15:54\n[buffer @ 0x2226dc0] w:480 h:272 pixfmt:yuv420p\n[scale @ 0x2225de0] w:480 h:272 fmt:yuv420p -> w:320 h:240 fmt:yuv420p flags:0x4\nThe bitrate parameter is set too low.It takes bits/s as argument, not kbits/s\n    Last message repeated 1 times\nOutput #0, avi, to \'media/videos/20120812_092359/092759-IMG_4718-job1.avi\':\n  Metadata:\n    major_brand     : qt  \n    minor_version   : 0\n    compatible_brands: qt  \n    creation_time   : 2012-08-05 08:15:54\n    date-fra        : 2012-08-05T10:15:35+0200\n    encoder-fra     : 5.1.1\n    ICRD            : 2012-08-05T10:15:35+0200\n    ISFT            : Lavf53.21.0\n    Stream #0.0(und): Video: mpeg4, yuv420p, 320x240, q=2-31, 0 kb/s, 30 tbn, 30 tbc\n    Metadata:\n      creation_time   : 2012-08-05 08:15:54\n    Stream #0.1(und): Audio: aac, 24000 Hz, mono, s16, 0 kb/s\n    Metadata:\n      creation_time   : 2012-08-05 08:15:54\nStream mapping:\n  Stream #0.1 -> #0.0\n  Stream #0.0 -> #0.1\nPress ctrl-c to stop encoding\nframe=  324 fps=  0 q=31.0 Lsize=     246kB time=10.80 bitrate= 186.6kbits/s    \r\nvideo:221kB audio:2kB global headers:0kB muxing overhead 10.516204%\n<br>'),(3,'sdfgsdfg',1,'C','2012-08-12 21:15:00','2012-08-12 21:15:01','','===== Log job1 =============================\n\nError log :\nffmpeg version 0.8.3-4:0.8.3-0ubuntu0.12.04.1, Copyright (c) 2000-2012 the Libav developers\n  built on Jun 12 2012 16:52:09 with gcc 4.6.3\n*** THIS PROGRAM IS DEPRECATED ***\nThis program is only provided for compatibility and will be removed in a future release. Please use avconv instead.\n\nSeems stream 1 codec frame rate differs from container frame rate: 1200.00 (1200/1) -> 30.00 (30/1)\nInput #0, mov,mp4,m4a,3gp,3g2,mj2, from \'media/videos/20120812_210324/IMG_4718.MOV\':\n  Metadata:\n    major_brand     : qt  \n    minor_version   : 0\n    compatible_brands: qt  \n    creation_time   : 2012-08-05 08:15:54\n    encoder         : 5.1.1\n    encoder-fra     : 5.1.1\n    date            : 2012-08-05T10:15:35+0200\n    date-fra        : 2012-08-05T10:15:35+0200\n  Duration: 00:00:10.80, start: 0.000000, bitrate: 807 kb/s\n    Stream #0.0(und): Audio: aac, 44100 Hz, mono, s16, 62 kb/s\n    Metadata:\n      creation_time   : 2012-08-05 08:15:54\n    Stream #0.1(und): Video: h264 (Main), yuv420p, 480x272, 740 kb/s, 30 fps, 30 tbr, 600 tbn, 1200 tbc\n    Metadata:\n      creation_time   : 2012-08-05 08:15:54\n[buffer @ 0x16e7dc0] w:480 h:272 pixfmt:yuv420p\n[scale @ 0x16e6de0] w:480 h:272 fmt:yuv420p -> w:320 h:240 fmt:yuv420p flags:0x4\nThe bitrate parameter is set too low.It takes bits/s as argument, not kbits/s\n    Last message repeated 1 times\nOutput #0, avi, to \'media/videos/20120812_210324/211500-IMG_4718-job1.avi\':\n  Metadata:\n    major_brand     : qt  \n    minor_version   : 0\n    compatible_brands: qt  \n    creation_time   : 2012-08-05 08:15:54\n    date-fra        : 2012-08-05T10:15:35+0200\n    encoder-fra     : 5.1.1\n    ICRD            : 2012-08-05T10:15:35+0200\n    ISFT            : Lavf53.21.0\n    Stream #0.0(und): Video: mpeg4, yuv420p, 320x240, q=2-31, 0 kb/s, 30 tbn, 30 tbc\n    Metadata:\n      creation_time   : 2012-08-05 08:15:54\n    Stream #0.1(und): Audio: aac, 24000 Hz, mono, s16, 0 kb/s\n    Metadata:\n      creation_time   : 2012-08-05 08:15:54\nStream mapping:\n  Stream #0.1 -> #0.0\n  Stream #0.0 -> #0.1\nPress ctrl-c to stop encoding\nframe=  324 fps=  0 q=31.0 Lsize=     246kB time=10.80 bitrate= 186.6kbits/s    \r\nvideo:221kB audio:2kB global headers:0kB muxing overhead 10.516204%\n===== Log qsdfqsdf =============================\n\nError log :\nffmpeg version 0.8.3-4:0.8.3-0ubuntu0.12.04.1, Copyright (c) 2000-2012 the Libav developers\n  built on Jun 12 2012 16:52:09 with gcc 4.6.3\n*** THIS PROGRAM IS DEPRECATED ***\nThis program is only provided for compatibility and will be removed in a future release. Please use avconv instead.\n\nSeems stream 1 codec frame rate differs from container frame rate: 1200.00 (1200/1) -> 30.00 (30/1)\nInput #0, mov,mp4,m4a,3gp,3g2,mj2, from \'media/videos/20120812_210324/IMG_4718.MOV\':\n  Metadata:\n    major_brand     : qt  \n    minor_version   : 0\n    compatible_brands: qt  \n    creation_time   : 2012-08-05 08:15:54\n    encoder         : 5.1.1\n    encoder-fra     : 5.1.1\n    date            : 2012-08-05T10:15:35+0200\n    date-fra        : 2012-08-05T10:15:35+0200\n  Duration: 00:00:10.80, start: 0.000000, bitrate: 807 kb/s\n    Stream #0.0(und): Audio: aac, 44100 Hz, mono, s16, 62 kb/s\n    Metadata:\n      creation_time   : 2012-08-05 08:15:54\n    Stream #0.1(und): Video: h264 (Main), yuv420p, 480x272, 740 kb/s, 30 fps, 30 tbr, 600 tbn, 1200 tbc\n    Metadata:\n      creation_time   : 2012-08-05 08:15:54\n[buffer @ 0x191ddc0] w:480 h:272 pixfmt:yuv420p\n[scale @ 0x191cde0] w:480 h:272 fmt:yuv420p -> w:320 h:240 fmt:yuv420p flags:0x4\nThe bitrate parameter is set too low.It takes bits/s as argument, not kbits/s\n    Last message repeated 1 times\nOutput #0, avi, to \'media/videos/20120812_210324/211500-IMG_4718-qsdfqsdf.avi\':\n  Metadata:\n    major_brand     : qt  \n    minor_version   : 0\n    compatible_brands: qt  \n    creation_time   : 2012-08-05 08:15:54\n    date-fra        : 2012-08-05T10:15:35+0200\n    encoder-fra     : 5.1.1\n    ICRD            : 2012-08-05T10:15:35+0200\n    ISFT            : Lavf53.21.0\n    Stream #0.0(und): Video: mpeg4, yuv420p, 320x240, q=2-31, 0 kb/s, 30 tbn, 30 tbc\n    Metadata:\n      creation_time   : 2012-08-05 08:15:54\n    Stream #0.1(und): Audio: aac, 24000 Hz, mono, s16, 0 kb/s\n    Metadata:\n      creation_time   : 2012-08-05 08:15:54\nStream mapping:\n  Stream #0.1 -> #0.0\n  Stream #0.0 -> #0.1\nPress ctrl-c to stop encoding\nframe=  324 fps=  0 q=31.0 Lsize=     246kB time=10.80 bitrate= 186.6kbits/s    \r\nvideo:221kB audio:2kB global headers:0kB muxing overhead 10.516204%\n');
/*!40000 ALTER TABLE `encoder_taskhistory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-08-12 21:22:18
