--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'EUC_JP';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: ad_user; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE ad_user (
    id character varying(20),
    pass character varying(20),
    allt integer,
    nyukai integer,
    idou integer,
    meibo integer,
    bansan integer,
    gyouji integer,
    jyukou integer,
    kougi integer,
    toiawase integer
);


ALTER TABLE public.ad_user OWNER TO postgres;

--
-- Name: bansan; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE bansan (
    kaisai character varying(15),
    namef character varying(50),
    name character varying(50),
    num character varying(10),
    sotunen character varying(10),
    gakubu character varying(50),
    mail character varying(150),
    id integer NOT NULL,
    day timestamp without time zone,
    delflg character varying(10)
);


ALTER TABLE public.bansan OWNER TO postgres;

--
-- Name: bansan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE bansan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.bansan_id_seq OWNER TO postgres;

--
-- Name: bansan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE bansan_id_seq OWNED BY bansan.id;


--
-- Name: gyouji; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE gyouji (
    kaisai character varying(15),
    gyouji character varying(160),
    namef character varying(50),
    name character varying(50),
    num character varying(10),
    sotunen character varying(10),
    gakubu character varying(50),
    mail character varying(150),
    id integer NOT NULL,
    day timestamp without time zone,
    delflg character varying(10)
);


ALTER TABLE public.gyouji OWNER TO postgres;

--
-- Name: gyouji_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE gyouji_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.gyouji_id_seq OWNER TO postgres;

--
-- Name: gyouji_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE gyouji_id_seq OWNED BY gyouji.id;


--
-- Name: idou; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE idou (
    namef character varying(50),
    name character varying(50),
    num character varying(10),
    sotunen character varying(10),
    gakubu character varying(50),
    cname character varying(100),
    cnameflg integer,
    ctel character varying(20),
    ctelflg integer,
    caddnum character varying(10),
    caddnumflg integer,
    cshozoku character varying(100),
    cshozokuflg integer,
    cadd character varying(160),
    caddflg integer,
    czaiseki character varying(100),
    czaisekiflg integer,
    tel character varying(20),
    telflg integer,
    addnum character varying(10),
    addnumflg integer,
    add character varying(160),
    addflg integer,
    bikou text,
    cfax character varying(20),
    cfaxflg integer,
    cmail character varying(150),
    cmailflg integer,
    fax character varying(20),
    faxflg integer,
    mail character varying(150),
    mailflg integer,
    mmail character varying(150),
    mmailflg integer,
    id integer NOT NULL,
    day timestamp without time zone,
    delflg character varying(10)
);


ALTER TABLE public.idou OWNER TO postgres;

--
-- Name: idou_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE idou_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.idou_id_seq OWNER TO postgres;

--
-- Name: idou_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE idou_id_seq OWNED BY idou.id;


--
-- Name: jukou; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE jukou (
    kaiki character varying(10),
    namef character varying(50),
    name character varying(50),
    num character varying(10),
    sotunen character varying(10),
    gakubu character varying(50),
    mail character varying(150),
    douki text,
    bikou text,
    id integer NOT NULL,
    day timestamp without time zone,
    delflg character varying(10)
);


ALTER TABLE public.jukou OWNER TO postgres;

--
-- Name: jukou_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE jukou_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.jukou_id_seq OWNER TO postgres;

--
-- Name: jukou_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE jukou_id_seq OWNED BY jukou.id;


--
-- Name: kougi; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE kougi (
    kaiki character varying(10),
    namef character varying(50),
    name character varying(50),
    num character varying(10),
    sotunen character varying(10),
    gakubu character varying(50),
    mail character varying(150),
    souhu character varying(20),
    bikou text,
    id integer NOT NULL,
    day timestamp without time zone,
    delflg character varying(10)
);


ALTER TABLE public.kougi OWNER TO postgres;

--
-- Name: kougi_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE kougi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.kougi_id_seq OWNER TO postgres;

--
-- Name: kougi_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE kougi_id_seq OWNED BY kougi.id;


--
-- Name: meibo; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE meibo (
    namef character varying(50),
    name character varying(50),
    num character varying(10),
    sotunen character varying(10),
    gakubu character varying(50),
    mail character varying(150),
    souhu character varying(20),
    meibo character varying(60),
    id integer NOT NULL,
    day timestamp without time zone,
    delflg character varying(10)
);


ALTER TABLE public.meibo OWNER TO postgres;

--
-- Name: meibo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE meibo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.meibo_id_seq OWNER TO postgres;

--
-- Name: meibo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE meibo_id_seq OWNED BY meibo.id;


--
-- Name: nyukai; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE nyukai (
    namef character varying(50),
    name character varying(50),
    sotunen character varying(10),
    gakubu character varying(50),
    addnum character varying(10),
    add character varying(160),
    tel character varying(20),
    mail character varying(150),
    bikou text,
    id integer NOT NULL,
    day timestamp without time zone,
    delflg character varying(10)
);


ALTER TABLE public.nyukai OWNER TO postgres;

--
-- Name: nyukai_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE nyukai_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.nyukai_id_seq OWNER TO postgres;

--
-- Name: nyukai_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE nyukai_id_seq OWNED BY nyukai.id;


--
-- Name: toiawase; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE toiawase (
    namef character varying(50),
    name character varying(50),
    num character varying(10),
    sotunen character varying(10),
    gakubu character varying(50),
    addnum character varying(10),
    add character varying(160),
    tel character varying(20),
    mail character varying(150),
    toiawase text,
    id integer NOT NULL,
    day timestamp without time zone,
    delflg character varying(10)
);


ALTER TABLE public.toiawase OWNER TO postgres;

--
-- Name: toiawase_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE toiawase_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.toiawase_id_seq OWNER TO postgres;

--
-- Name: toiawase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE toiawase_id_seq OWNED BY toiawase.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY bansan ALTER COLUMN id SET DEFAULT nextval('bansan_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY gyouji ALTER COLUMN id SET DEFAULT nextval('gyouji_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY idou ALTER COLUMN id SET DEFAULT nextval('idou_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY jukou ALTER COLUMN id SET DEFAULT nextval('jukou_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY kougi ALTER COLUMN id SET DEFAULT nextval('kougi_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY meibo ALTER COLUMN id SET DEFAULT nextval('meibo_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY nyukai ALTER COLUMN id SET DEFAULT nextval('nyukai_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY toiawase ALTER COLUMN id SET DEFAULT nextval('toiawase_id_seq'::regclass);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: ad_user; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE ad_user FROM PUBLIC;
REVOKE ALL ON TABLE ad_user FROM postgres;
GRANT ALL ON TABLE ad_user TO postgres;
GRANT ALL ON TABLE ad_user TO "www-data";


--
-- Name: bansan; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE bansan FROM PUBLIC;
REVOKE ALL ON TABLE bansan FROM postgres;
GRANT ALL ON TABLE bansan TO postgres;
GRANT ALL ON TABLE bansan TO "www-data";


--
-- Name: bansan_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE bansan_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE bansan_id_seq FROM postgres;
GRANT ALL ON SEQUENCE bansan_id_seq TO postgres;
GRANT ALL ON SEQUENCE bansan_id_seq TO "www-data";


--
-- Name: gyouji; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE gyouji FROM PUBLIC;
REVOKE ALL ON TABLE gyouji FROM postgres;
GRANT ALL ON TABLE gyouji TO postgres;
GRANT ALL ON TABLE gyouji TO "www-data";


--
-- Name: gyouji_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE gyouji_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE gyouji_id_seq FROM postgres;
GRANT ALL ON SEQUENCE gyouji_id_seq TO postgres;
GRANT ALL ON SEQUENCE gyouji_id_seq TO "www-data";


--
-- Name: idou; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE idou FROM PUBLIC;
REVOKE ALL ON TABLE idou FROM postgres;
GRANT ALL ON TABLE idou TO postgres;
GRANT ALL ON TABLE idou TO "www-data";


--
-- Name: idou_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE idou_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE idou_id_seq FROM postgres;
GRANT ALL ON SEQUENCE idou_id_seq TO postgres;
GRANT ALL ON SEQUENCE idou_id_seq TO "www-data";


--
-- Name: jukou; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE jukou FROM PUBLIC;
REVOKE ALL ON TABLE jukou FROM postgres;
GRANT ALL ON TABLE jukou TO postgres;
GRANT ALL ON TABLE jukou TO "www-data";


--
-- Name: jukou_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE jukou_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE jukou_id_seq FROM postgres;
GRANT ALL ON SEQUENCE jukou_id_seq TO postgres;
GRANT ALL ON SEQUENCE jukou_id_seq TO "www-data";


--
-- Name: kougi; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE kougi FROM PUBLIC;
REVOKE ALL ON TABLE kougi FROM postgres;
GRANT ALL ON TABLE kougi TO postgres;
GRANT ALL ON TABLE kougi TO "www-data";


--
-- Name: kougi_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE kougi_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE kougi_id_seq FROM postgres;
GRANT ALL ON SEQUENCE kougi_id_seq TO postgres;
GRANT ALL ON SEQUENCE kougi_id_seq TO "www-data";


--
-- Name: meibo; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE meibo FROM PUBLIC;
REVOKE ALL ON TABLE meibo FROM postgres;
GRANT ALL ON TABLE meibo TO postgres;
GRANT ALL ON TABLE meibo TO "www-data";


--
-- Name: meibo_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE meibo_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE meibo_id_seq FROM postgres;
GRANT ALL ON SEQUENCE meibo_id_seq TO postgres;
GRANT ALL ON SEQUENCE meibo_id_seq TO "www-data";


--
-- Name: nyukai; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE nyukai FROM PUBLIC;
REVOKE ALL ON TABLE nyukai FROM postgres;
GRANT ALL ON TABLE nyukai TO postgres;
GRANT ALL ON TABLE nyukai TO "www-data";


--
-- Name: nyukai_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE nyukai_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE nyukai_id_seq FROM postgres;
GRANT ALL ON SEQUENCE nyukai_id_seq TO postgres;
GRANT ALL ON SEQUENCE nyukai_id_seq TO "www-data";


--
-- Name: toiawase; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE toiawase FROM PUBLIC;
REVOKE ALL ON TABLE toiawase FROM postgres;
GRANT ALL ON TABLE toiawase TO postgres;
GRANT ALL ON TABLE toiawase TO "www-data";


--
-- Name: toiawase_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE toiawase_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE toiawase_id_seq FROM postgres;
GRANT ALL ON SEQUENCE toiawase_id_seq TO postgres;
GRANT ALL ON SEQUENCE toiawase_id_seq TO "www-data";


--
-- PostgreSQL database dump complete
--

