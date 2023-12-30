--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.0

-- Started on 2023-12-31 00:29:38

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 25813)
-- Name: ca_procedure; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ca_procedure (
    duration integer NOT NULL,
    applied_potential double precision NOT NULL,
    interval_time double precision NOT NULL,
    capacity double precision,
    diffusion_coefficient double precision,
    procedure_id bigint NOT NULL,
    ca_measurment_id bigint NOT NULL,
    reaction_order integer,
    reaction_rate_constant double precision
);


ALTER TABLE public.ca_procedure OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 25816)
-- Name: ca_procedure_ca_measurment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ca_procedure_ca_measurment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ca_procedure_ca_measurment_id_seq OWNER TO postgres;

--
-- TOC entry 4970 (class 0 OID 0)
-- Dependencies: 216
-- Name: ca_procedure_ca_measurment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ca_procedure_ca_measurment_id_seq OWNED BY public.ca_procedure.ca_measurment_id;


--
-- TOC entry 217 (class 1259 OID 25817)
-- Name: ca_procedure_procedure_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ca_procedure_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ca_procedure_procedure_id_seq OWNER TO postgres;

--
-- TOC entry 4971 (class 0 OID 0)
-- Dependencies: 217
-- Name: ca_procedure_procedure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ca_procedure_procedure_id_seq OWNED BY public.ca_procedure.procedure_id;


--
-- TOC entry 218 (class 1259 OID 25818)
-- Name: ca_raw; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ca_raw (
    corrected_time double precision,
    charge double precision,
    current double precision,
    potential double precision,
    power double precision,
    dcharge_dt double precision,
    dpotential_dt double precision,
    dpower_dt double precision,
    index double precision,
    procedure_id bigint NOT NULL,
    raw_id bigint NOT NULL,
    dcurrent_dt double precision
);


ALTER TABLE public.ca_raw OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 25821)
-- Name: ca_raw_procedure_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ca_raw_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ca_raw_procedure_id_seq OWNER TO postgres;

--
-- TOC entry 4972 (class 0 OID 0)
-- Dependencies: 219
-- Name: ca_raw_procedure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ca_raw_procedure_id_seq OWNED BY public.ca_raw.procedure_id;


--
-- TOC entry 220 (class 1259 OID 25822)
-- Name: ca_raw_raw_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ca_raw_raw_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ca_raw_raw_id_seq OWNER TO postgres;

--
-- TOC entry 4973 (class 0 OID 0)
-- Dependencies: 220
-- Name: ca_raw_raw_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ca_raw_raw_id_seq OWNED BY public.ca_raw.raw_id;


--
-- TOC entry 221 (class 1259 OID 25823)
-- Name: cp_procedure; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cp_procedure (
    duration integer NOT NULL,
    applied_current double precision NOT NULL,
    interval_time double precision NOT NULL,
    initial_transition_time double precision,
    procedure_id bigint NOT NULL,
    cp_measurment_id bigint NOT NULL,
    initial_transition_potential double precision
);


ALTER TABLE public.cp_procedure OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 25826)
-- Name: cp_procedure_cp_measurment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cp_procedure_cp_measurment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cp_procedure_cp_measurment_id_seq OWNER TO postgres;

--
-- TOC entry 4974 (class 0 OID 0)
-- Dependencies: 222
-- Name: cp_procedure_cp_measurment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cp_procedure_cp_measurment_id_seq OWNED BY public.cp_procedure.cp_measurment_id;


--
-- TOC entry 223 (class 1259 OID 25827)
-- Name: cp_procedure_procedure_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cp_procedure_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cp_procedure_procedure_id_seq OWNER TO postgres;

--
-- TOC entry 4975 (class 0 OID 0)
-- Dependencies: 223
-- Name: cp_procedure_procedure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cp_procedure_procedure_id_seq OWNED BY public.cp_procedure.procedure_id;


--
-- TOC entry 224 (class 1259 OID 25828)
-- Name: cp_raw; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cp_raw (
    corrected_time double precision,
    charge double precision,
    current double precision,
    potential double precision,
    power double precision,
    dcurrent_dt double precision,
    index double precision,
    procedure_id bigint NOT NULL,
    raw_id bigint NOT NULL,
    dcharge_dt double precision,
    dpotential_dt double precision,
    dpower_dt double precision
);


ALTER TABLE public.cp_raw OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 25831)
-- Name: cp_raw_procedure_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cp_raw_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cp_raw_procedure_id_seq OWNER TO postgres;

--
-- TOC entry 4976 (class 0 OID 0)
-- Dependencies: 225
-- Name: cp_raw_procedure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cp_raw_procedure_id_seq OWNED BY public.cp_raw.procedure_id;


--
-- TOC entry 226 (class 1259 OID 25832)
-- Name: cp_raw_raw_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cp_raw_raw_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cp_raw_raw_id_seq OWNER TO postgres;

--
-- TOC entry 4977 (class 0 OID 0)
-- Dependencies: 226
-- Name: cp_raw_raw_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cp_raw_raw_id_seq OWNED BY public.cp_raw.raw_id;


--
-- TOC entry 227 (class 1259 OID 25833)
-- Name: cv_cycle; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cv_cycle (
    cycle_number smallint NOT NULL,
    peaks_anodic double precision[],
    peaks_cathodic double precision[],
    d_anodic double precision[],
    e_half double precision[],
    h_anodic double precision[],
    h_cathodic double precision[],
    corrosion_point double precision[],
    procedure_id bigint NOT NULL,
    cycle_id smallint NOT NULL,
    d_cathodic double precision[],
    temperature double precision NOT NULL
);


ALTER TABLE public.cv_cycle OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 25838)
-- Name: cv_cycle_cycle_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cv_cycle_cycle_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cv_cycle_cycle_id_seq OWNER TO postgres;

--
-- TOC entry 4978 (class 0 OID 0)
-- Dependencies: 228
-- Name: cv_cycle_cycle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cv_cycle_cycle_id_seq OWNED BY public.cv_cycle.cycle_id;


--
-- TOC entry 229 (class 1259 OID 25839)
-- Name: cv_cycle_procedure_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cv_cycle_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cv_cycle_procedure_id_seq OWNER TO postgres;

--
-- TOC entry 4979 (class 0 OID 0)
-- Dependencies: 229
-- Name: cv_cycle_procedure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cv_cycle_procedure_id_seq OWNED BY public.cv_cycle.procedure_id;


--
-- TOC entry 230 (class 1259 OID 25840)
-- Name: cv_staircase_procedure_cv_measurment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cv_staircase_procedure_cv_measurment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cv_staircase_procedure_cv_measurment_id_seq OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 25841)
-- Name: cv_staircase_procedure_procedure_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cv_staircase_procedure_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cv_staircase_procedure_procedure_id_seq OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 25842)
-- Name: cv_staircase_procedure; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cv_staircase_procedure (
    start_potential double precision NOT NULL,
    upper_vertex double precision NOT NULL,
    lower_vertex double precision NOT NULL,
    step_size double precision NOT NULL,
    num_of_stop_crossings double precision NOT NULL,
    stop_value double precision NOT NULL,
    scan_rate double precision NOT NULL,
    procedure_id bigint DEFAULT nextval('public.cv_staircase_procedure_procedure_id_seq'::regclass) NOT NULL,
    cv_measurment_id bigint DEFAULT nextval('public.cv_staircase_procedure_cv_measurment_id_seq'::regclass) NOT NULL
);


ALTER TABLE public.cv_staircase_procedure OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 25847)
-- Name: cv_staircase_raw_procedure_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cv_staircase_raw_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cv_staircase_raw_procedure_id_seq OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 25848)
-- Name: cv_staircase_raw_raw_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cv_staircase_raw_raw_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cv_staircase_raw_raw_id_seq OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 25849)
-- Name: cv_staircase_raw; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cv_staircase_raw (
    potential_applied double precision NOT NULL,
    current double precision NOT NULL,
    scan_number double precision NOT NULL,
    index double precision NOT NULL,
    power double precision NOT NULL,
    resistance double precision NOT NULL,
    charge double precision NOT NULL,
    dcurrent_dt double precision NOT NULL,
    dcharge_dt double precision NOT NULL,
    procedure_id bigint DEFAULT nextval('public.cv_staircase_raw_procedure_id_seq'::regclass) NOT NULL,
    raw_id bigint DEFAULT nextval('public.cv_staircase_raw_raw_id_seq'::regclass) NOT NULL,
    potential double precision
);


ALTER TABLE public.cv_staircase_raw OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 25854)
-- Name: eis_procedure; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.eis_procedure (
    potential double precision NOT NULL,
    lower_freuqency double precision NOT NULL,
    upper_frequency double precision NOT NULL,
    potential_dc double precision,
    current_dc double precision,
    procedure_id bigint NOT NULL,
    eis_measurment_id bigint NOT NULL
);


ALTER TABLE public.eis_procedure OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 25857)
-- Name: eis_procedure_eis_measurment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.eis_procedure_eis_measurment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.eis_procedure_eis_measurment_id_seq OWNER TO postgres;

--
-- TOC entry 4980 (class 0 OID 0)
-- Dependencies: 237
-- Name: eis_procedure_eis_measurment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.eis_procedure_eis_measurment_id_seq OWNED BY public.eis_procedure.eis_measurment_id;


--
-- TOC entry 238 (class 1259 OID 25858)
-- Name: eis_procedure_procedure_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.eis_procedure_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.eis_procedure_procedure_id_seq OWNER TO postgres;

--
-- TOC entry 4981 (class 0 OID 0)
-- Dependencies: 238
-- Name: eis_procedure_procedure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.eis_procedure_procedure_id_seq OWNED BY public.eis_procedure.procedure_id;


--
-- TOC entry 239 (class 1259 OID 25859)
-- Name: eis_raw; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.eis_raw (
    frequency double precision NOT NULL,
    z_real double precision NOT NULL,
    neg_z_imag double precision NOT NULL,
    z_norm double precision NOT NULL,
    neg_phase_shift double precision,
    procedure_id bigint NOT NULL,
    raw_id bigint NOT NULL,
    index bigint
);


ALTER TABLE public.eis_raw OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 25862)
-- Name: eis_raw_procedure_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.eis_raw_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.eis_raw_procedure_id_seq OWNER TO postgres;

--
-- TOC entry 4982 (class 0 OID 0)
-- Dependencies: 240
-- Name: eis_raw_procedure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.eis_raw_procedure_id_seq OWNED BY public.eis_raw.procedure_id;


--
-- TOC entry 241 (class 1259 OID 25863)
-- Name: eis_raw_raw_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.eis_raw_raw_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.eis_raw_raw_id_seq OWNER TO postgres;

--
-- TOC entry 4983 (class 0 OID 0)
-- Dependencies: 241
-- Name: eis_raw_raw_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.eis_raw_raw_id_seq OWNED BY public.eis_raw.raw_id;


--
-- TOC entry 242 (class 1259 OID 25864)
-- Name: experiments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.experiments (
    experiment_id integer NOT NULL,
    material character varying(100) NOT NULL,
    date date NOT NULL,
    user_id integer NOT NULL,
    start_time time without time zone,
    number_of_electrons bigint NOT NULL,
    electrode_area double precision,
    concentration_of_active_material double precision,
    mass_of_active_material double precision,
    duration time without time zone
);


ALTER TABLE public.experiments OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 25867)
-- Name: experiment_experiment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.experiment_experiment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.experiment_experiment_id_seq OWNER TO postgres;

--
-- TOC entry 4984 (class 0 OID 0)
-- Dependencies: 243
-- Name: experiment_experiment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.experiment_experiment_id_seq OWNED BY public.experiments.experiment_id;


--
-- TOC entry 244 (class 1259 OID 25868)
-- Name: experiment_user_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.experiment_user_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.experiment_user_seq OWNER TO postgres;

--
-- TOC entry 4985 (class 0 OID 0)
-- Dependencies: 244
-- Name: experiment_user_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.experiment_user_seq OWNED BY public.experiments.user_id;


--
-- TOC entry 245 (class 1259 OID 25869)
-- Name: measurements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.measurements (
    measurement_id bigint NOT NULL,
    procedure_name character varying(20) NOT NULL,
    experiment_id bigint NOT NULL
);


ALTER TABLE public.measurements OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 25872)
-- Name: measurment_experiment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.measurment_experiment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.measurment_experiment_id_seq OWNER TO postgres;

--
-- TOC entry 4986 (class 0 OID 0)
-- Dependencies: 246
-- Name: measurment_experiment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.measurment_experiment_id_seq OWNED BY public.measurements.experiment_id;


--
-- TOC entry 247 (class 1259 OID 25873)
-- Name: measurment_measurment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.measurment_measurment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.measurment_measurment_id_seq OWNER TO postgres;

--
-- TOC entry 4987 (class 0 OID 0)
-- Dependencies: 247
-- Name: measurment_measurment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.measurment_measurment_id_seq OWNED BY public.measurements.measurement_id;


--
-- TOC entry 248 (class 1259 OID 25874)
-- Name: motor_positions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.motor_positions (
    x_coordinate double precision,
    y_coordinate double precision,
    experiment_id integer NOT NULL,
    z_coordinate double precision
);


ALTER TABLE public.motor_positions OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 25877)
-- Name: motor_experiment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.motor_experiment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.motor_experiment_id_seq OWNER TO postgres;

--
-- TOC entry 4988 (class 0 OID 0)
-- Dependencies: 249
-- Name: motor_experiment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.motor_experiment_id_seq OWNED BY public.motor_positions.experiment_id;


--
-- TOC entry 250 (class 1259 OID 25878)
-- Name: ocp_procedure; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ocp_procedure (
    duration integer,
    interval_time double precision,
    procedure_id integer NOT NULL,
    ocp_measurment_id bigint NOT NULL
);


ALTER TABLE public.ocp_procedure OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 25881)
-- Name: ocp_procedure_ocp_measurment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ocp_procedure_ocp_measurment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ocp_procedure_ocp_measurment_id_seq OWNER TO postgres;

--
-- TOC entry 4989 (class 0 OID 0)
-- Dependencies: 251
-- Name: ocp_procedure_ocp_measurment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ocp_procedure_ocp_measurment_id_seq OWNED BY public.ocp_procedure.ocp_measurment_id;


--
-- TOC entry 252 (class 1259 OID 25882)
-- Name: ocp_procedure_procedure_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ocp_procedure_procedure_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ocp_procedure_procedure_id_seq OWNER TO postgres;

--
-- TOC entry 4990 (class 0 OID 0)
-- Dependencies: 252
-- Name: ocp_procedure_procedure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ocp_procedure_procedure_id_seq OWNED BY public.ocp_procedure.procedure_id;


--
-- TOC entry 253 (class 1259 OID 25883)
-- Name: ocp_raw; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ocp_raw (
    corrected_time double precision,
    charge double precision,
    current double precision,
    potential double precision,
    power double precision,
    dcharge_dt double precision,
    dpotential_dt double precision,
    dpower_dt double precision,
    procedure_id integer NOT NULL,
    raw_id bigint NOT NULL,
    index double precision
);


ALTER TABLE public.ocp_raw OWNER TO postgres;

--
-- TOC entry 254 (class 1259 OID 25886)
-- Name: ocp_raw_ocp_procedure_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ocp_raw_ocp_procedure_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ocp_raw_ocp_procedure_id_seq OWNER TO postgres;

--
-- TOC entry 4991 (class 0 OID 0)
-- Dependencies: 254
-- Name: ocp_raw_ocp_procedure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ocp_raw_ocp_procedure_id_seq OWNED BY public.ocp_raw.procedure_id;


--
-- TOC entry 255 (class 1259 OID 25887)
-- Name: ocp_raw_raw_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ocp_raw_raw_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ocp_raw_raw_id_seq OWNER TO postgres;

--
-- TOC entry 4992 (class 0 OID 0)
-- Dependencies: 255
-- Name: ocp_raw_raw_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ocp_raw_raw_id_seq OWNED BY public.ocp_raw.raw_id;


--
-- TOC entry 256 (class 1259 OID 25888)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(50) NOT NULL,
    password character varying,
    username character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 25893)
-- Name: user_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_user_id_seq OWNER TO postgres;

--
-- TOC entry 4993 (class 0 OID 0)
-- Dependencies: 257
-- Name: user_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_user_id_seq OWNED BY public.users.user_id;


--
-- TOC entry 259 (class 1259 OID 26027)
-- Name: xps_c1s_raw; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.xps_c1s_raw (
    "c=c" double precision,
    "c-c" double precision,
    "c-o" double precision,
    "c=o" double precision,
    "o-c=o" double precision,
    co3 double precision,
    background_cps double precision,
    envelope_cps double precision,
    cps double precision,
    raw_id bigint NOT NULL,
    procedure_id bigint
);


ALTER TABLE public.xps_c1s_raw OWNER TO postgres;

--
-- TOC entry 260 (class 1259 OID 26037)
-- Name: xps_f1s_raw; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.xps_f1s_raw (
    cps double precision,
    lif double precision,
    lipf6 double precision,
    background_cps double precision,
    envelope_cps double precision,
    raw_id bigint NOT NULL,
    procedure_id bigint,
    lixpfyoz double precision
);


ALTER TABLE public.xps_f1s_raw OWNER TO postgres;

--
-- TOC entry 261 (class 1259 OID 26047)
-- Name: xps_li1s_raw; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.xps_li1s_raw (
    cps double precision,
    lif double precision,
    background_cps double precision,
    envelope_cps double precision,
    raw_id bigint NOT NULL,
    procedure_id bigint
);


ALTER TABLE public.xps_li1s_raw OWNER TO postgres;

--
-- TOC entry 262 (class 1259 OID 26062)
-- Name: xps_o1s_raw; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.xps_o1s_raw (
    cps double precision,
    "c-o" double precision,
    lixpfyoz double precision,
    background_cps double precision,
    envelope_cps double precision,
    raw_id bigint NOT NULL,
    procedure_id bigint
);


ALTER TABLE public.xps_o1s_raw OWNER TO postgres;

--
-- TOC entry 258 (class 1259 OID 26017)
-- Name: xps_procedure; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.xps_procedure (
    ds_pass_energy double precision,
    ds_dwell_time double precision,
    ds_step_size double precision,
    ss_pass_energy double precision,
    ss_dwell_time double precision,
    ss_step_size double precision,
    emission double precision,
    power double precision,
    source_energy double precision,
    procedure_id bigint NOT NULL,
    xps_measurement_id bigint
);


ALTER TABLE public.xps_procedure OWNER TO postgres;

--
-- TOC entry 4737 (class 2604 OID 25894)
-- Name: ca_procedure procedure_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ca_procedure ALTER COLUMN procedure_id SET DEFAULT nextval('public.ca_procedure_procedure_id_seq'::regclass);


--
-- TOC entry 4738 (class 2604 OID 25895)
-- Name: ca_procedure ca_measurment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ca_procedure ALTER COLUMN ca_measurment_id SET DEFAULT nextval('public.ca_procedure_ca_measurment_id_seq'::regclass);


--
-- TOC entry 4739 (class 2604 OID 25896)
-- Name: ca_raw procedure_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ca_raw ALTER COLUMN procedure_id SET DEFAULT nextval('public.ca_raw_procedure_id_seq'::regclass);


--
-- TOC entry 4740 (class 2604 OID 25897)
-- Name: ca_raw raw_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ca_raw ALTER COLUMN raw_id SET DEFAULT nextval('public.ca_raw_raw_id_seq'::regclass);


--
-- TOC entry 4741 (class 2604 OID 25898)
-- Name: cp_procedure procedure_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cp_procedure ALTER COLUMN procedure_id SET DEFAULT nextval('public.cp_procedure_procedure_id_seq'::regclass);


--
-- TOC entry 4742 (class 2604 OID 25899)
-- Name: cp_procedure cp_measurment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cp_procedure ALTER COLUMN cp_measurment_id SET DEFAULT nextval('public.cp_procedure_cp_measurment_id_seq'::regclass);


--
-- TOC entry 4743 (class 2604 OID 25900)
-- Name: cp_raw procedure_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cp_raw ALTER COLUMN procedure_id SET DEFAULT nextval('public.cp_raw_procedure_id_seq'::regclass);


--
-- TOC entry 4744 (class 2604 OID 25901)
-- Name: cp_raw raw_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cp_raw ALTER COLUMN raw_id SET DEFAULT nextval('public.cp_raw_raw_id_seq'::regclass);


--
-- TOC entry 4745 (class 2604 OID 25902)
-- Name: cv_cycle procedure_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cv_cycle ALTER COLUMN procedure_id SET DEFAULT nextval('public.cv_cycle_procedure_id_seq'::regclass);


--
-- TOC entry 4746 (class 2604 OID 25903)
-- Name: cv_cycle cycle_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cv_cycle ALTER COLUMN cycle_id SET DEFAULT nextval('public.cv_cycle_cycle_id_seq'::regclass);


--
-- TOC entry 4751 (class 2604 OID 25904)
-- Name: eis_procedure procedure_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eis_procedure ALTER COLUMN procedure_id SET DEFAULT nextval('public.eis_procedure_procedure_id_seq'::regclass);


--
-- TOC entry 4752 (class 2604 OID 25905)
-- Name: eis_procedure eis_measurment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eis_procedure ALTER COLUMN eis_measurment_id SET DEFAULT nextval('public.eis_procedure_eis_measurment_id_seq'::regclass);


--
-- TOC entry 4753 (class 2604 OID 25906)
-- Name: eis_raw procedure_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eis_raw ALTER COLUMN procedure_id SET DEFAULT nextval('public.eis_raw_procedure_id_seq'::regclass);


--
-- TOC entry 4754 (class 2604 OID 25907)
-- Name: eis_raw raw_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eis_raw ALTER COLUMN raw_id SET DEFAULT nextval('public.eis_raw_raw_id_seq'::regclass);


--
-- TOC entry 4755 (class 2604 OID 25908)
-- Name: experiments experiment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.experiments ALTER COLUMN experiment_id SET DEFAULT nextval('public.experiment_experiment_id_seq'::regclass);


--
-- TOC entry 4756 (class 2604 OID 25909)
-- Name: experiments user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.experiments ALTER COLUMN user_id SET DEFAULT nextval('public.experiment_user_seq'::regclass);


--
-- TOC entry 4757 (class 2604 OID 25910)
-- Name: measurements measurement_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.measurements ALTER COLUMN measurement_id SET DEFAULT nextval('public.measurment_measurment_id_seq'::regclass);


--
-- TOC entry 4758 (class 2604 OID 25911)
-- Name: measurements experiment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.measurements ALTER COLUMN experiment_id SET DEFAULT nextval('public.measurment_experiment_id_seq'::regclass);


--
-- TOC entry 4759 (class 2604 OID 25912)
-- Name: motor_positions experiment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.motor_positions ALTER COLUMN experiment_id SET DEFAULT nextval('public.motor_experiment_id_seq'::regclass);


--
-- TOC entry 4760 (class 2604 OID 25913)
-- Name: ocp_procedure procedure_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ocp_procedure ALTER COLUMN procedure_id SET DEFAULT nextval('public.ocp_procedure_procedure_id_seq'::regclass);


--
-- TOC entry 4761 (class 2604 OID 25914)
-- Name: ocp_procedure ocp_measurment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ocp_procedure ALTER COLUMN ocp_measurment_id SET DEFAULT nextval('public.ocp_procedure_ocp_measurment_id_seq'::regclass);


--
-- TOC entry 4762 (class 2604 OID 25915)
-- Name: ocp_raw procedure_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ocp_raw ALTER COLUMN procedure_id SET DEFAULT nextval('public.ocp_raw_ocp_procedure_id_seq'::regclass);


--
-- TOC entry 4763 (class 2604 OID 25916)
-- Name: ocp_raw raw_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ocp_raw ALTER COLUMN raw_id SET DEFAULT nextval('public.ocp_raw_raw_id_seq'::regclass);


--
-- TOC entry 4764 (class 2604 OID 25917)
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.user_user_id_seq'::regclass);


--
-- TOC entry 4766 (class 2606 OID 25919)
-- Name: ca_procedure ca_procedure_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ca_procedure
    ADD CONSTRAINT ca_procedure_pkey PRIMARY KEY (procedure_id);


--
-- TOC entry 4768 (class 2606 OID 25921)
-- Name: ca_raw ca_raw_to_id_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ca_raw
    ADD CONSTRAINT ca_raw_to_id_pkey PRIMARY KEY (raw_id);


--
-- TOC entry 4770 (class 2606 OID 25923)
-- Name: cp_procedure cp_procedure_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cp_procedure
    ADD CONSTRAINT cp_procedure_pkey PRIMARY KEY (procedure_id);


--
-- TOC entry 4772 (class 2606 OID 25925)
-- Name: cp_raw cp_raw_to_id_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cp_raw
    ADD CONSTRAINT cp_raw_to_id_pkey PRIMARY KEY (raw_id);


--
-- TOC entry 4774 (class 2606 OID 25927)
-- Name: cv_cycle cv_cycle_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cv_cycle
    ADD CONSTRAINT cv_cycle_pkey PRIMARY KEY (cycle_id);


--
-- TOC entry 4776 (class 2606 OID 25929)
-- Name: cv_staircase_procedure cv_procedure_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cv_staircase_procedure
    ADD CONSTRAINT cv_procedure_pkey PRIMARY KEY (procedure_id);


--
-- TOC entry 4778 (class 2606 OID 25931)
-- Name: cv_staircase_raw cv_raw_to_id_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cv_staircase_raw
    ADD CONSTRAINT cv_raw_to_id_pkey PRIMARY KEY (raw_id);


--
-- TOC entry 4780 (class 2606 OID 25933)
-- Name: eis_procedure eis_procedure_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eis_procedure
    ADD CONSTRAINT eis_procedure_pkey PRIMARY KEY (procedure_id);


--
-- TOC entry 4782 (class 2606 OID 25935)
-- Name: eis_raw eis_raw_to_id_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eis_raw
    ADD CONSTRAINT eis_raw_to_id_pkey PRIMARY KEY (raw_id);


--
-- TOC entry 4784 (class 2606 OID 25937)
-- Name: experiments experiment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.experiments
    ADD CONSTRAINT experiment_pkey PRIMARY KEY (experiment_id);


--
-- TOC entry 4786 (class 2606 OID 25939)
-- Name: measurements measurment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.measurements
    ADD CONSTRAINT measurment_pkey PRIMARY KEY (measurement_id);


--
-- TOC entry 4788 (class 2606 OID 25941)
-- Name: ocp_procedure ocp_procedure_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ocp_procedure
    ADD CONSTRAINT ocp_procedure_pkey PRIMARY KEY (procedure_id);


--
-- TOC entry 4790 (class 2606 OID 25943)
-- Name: ocp_raw ocp_raw_id_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ocp_raw
    ADD CONSTRAINT ocp_raw_id_pkey PRIMARY KEY (raw_id);


--
-- TOC entry 4792 (class 2606 OID 25945)
-- Name: users user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);


--
-- TOC entry 4796 (class 2606 OID 26031)
-- Name: xps_c1s_raw xps_c1s_raw_id_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.xps_c1s_raw
    ADD CONSTRAINT xps_c1s_raw_id_pkey PRIMARY KEY (raw_id);


--
-- TOC entry 4798 (class 2606 OID 26041)
-- Name: xps_f1s_raw xps_f1s_raw_id_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.xps_f1s_raw
    ADD CONSTRAINT xps_f1s_raw_id_pkey PRIMARY KEY (raw_id);


--
-- TOC entry 4800 (class 2606 OID 26051)
-- Name: xps_li1s_raw xps_li1s_raw_id_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.xps_li1s_raw
    ADD CONSTRAINT xps_li1s_raw_id_pkey PRIMARY KEY (raw_id);


--
-- TOC entry 4802 (class 2606 OID 26066)
-- Name: xps_o1s_raw xps_o1s_raw_id_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.xps_o1s_raw
    ADD CONSTRAINT xps_o1s_raw_id_pkey PRIMARY KEY (raw_id);


--
-- TOC entry 4794 (class 2606 OID 26021)
-- Name: xps_procedure xps_procedure_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.xps_procedure
    ADD CONSTRAINT xps_procedure_pkey PRIMARY KEY (procedure_id);


--
-- TOC entry 4803 (class 2606 OID 25946)
-- Name: ca_procedure ca_measrument_to_measurment_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ca_procedure
    ADD CONSTRAINT ca_measrument_to_measurment_id FOREIGN KEY (ca_measurment_id) REFERENCES public.measurements(measurement_id) NOT VALID;


--
-- TOC entry 4804 (class 2606 OID 25951)
-- Name: ca_raw ca_raw_to_ca_procedure; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ca_raw
    ADD CONSTRAINT ca_raw_to_ca_procedure FOREIGN KEY (procedure_id) REFERENCES public.ca_procedure(procedure_id) NOT VALID;


--
-- TOC entry 4805 (class 2606 OID 25956)
-- Name: cp_procedure cp_measrument_to_measurment_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cp_procedure
    ADD CONSTRAINT cp_measrument_to_measurment_id FOREIGN KEY (cp_measurment_id) REFERENCES public.measurements(measurement_id) NOT VALID;


--
-- TOC entry 4806 (class 2606 OID 25961)
-- Name: cp_raw cp_raw_to_cp_procedure; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cp_raw
    ADD CONSTRAINT cp_raw_to_cp_procedure FOREIGN KEY (procedure_id) REFERENCES public.cp_procedure(procedure_id) NOT VALID;


--
-- TOC entry 4807 (class 2606 OID 25966)
-- Name: cv_cycle cv_cycle_to_cv_procedure; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cv_cycle
    ADD CONSTRAINT cv_cycle_to_cv_procedure FOREIGN KEY (procedure_id) REFERENCES public.cv_staircase_procedure(procedure_id) NOT VALID;


--
-- TOC entry 4808 (class 2606 OID 25971)
-- Name: cv_staircase_procedure cv_measrument_to_measurment_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cv_staircase_procedure
    ADD CONSTRAINT cv_measrument_to_measurment_id FOREIGN KEY (cv_measurment_id) REFERENCES public.measurements(measurement_id) NOT VALID;


--
-- TOC entry 4809 (class 2606 OID 25976)
-- Name: cv_staircase_raw cv_raw_to_cv_procedure; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cv_staircase_raw
    ADD CONSTRAINT cv_raw_to_cv_procedure FOREIGN KEY (procedure_id) REFERENCES public.cv_staircase_procedure(procedure_id) NOT VALID;


--
-- TOC entry 4810 (class 2606 OID 25981)
-- Name: eis_procedure eis_measrument_to_measurment_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eis_procedure
    ADD CONSTRAINT eis_measrument_to_measurment_id FOREIGN KEY (eis_measurment_id) REFERENCES public.measurements(measurement_id) NOT VALID;


--
-- TOC entry 4811 (class 2606 OID 25986)
-- Name: eis_raw eis_raw_to_eis_procedure; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eis_raw
    ADD CONSTRAINT eis_raw_to_eis_procedure FOREIGN KEY (procedure_id) REFERENCES public.eis_procedure(procedure_id) NOT VALID;


--
-- TOC entry 4814 (class 2606 OID 25991)
-- Name: motor_positions experiment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.motor_positions
    ADD CONSTRAINT experiment FOREIGN KEY (experiment_id) REFERENCES public.experiments(experiment_id);


--
-- TOC entry 4813 (class 2606 OID 25996)
-- Name: measurements measurment_id_to_experiment_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.measurements
    ADD CONSTRAINT measurment_id_to_experiment_id FOREIGN KEY (experiment_id) REFERENCES public.experiments(experiment_id);


--
-- TOC entry 4815 (class 2606 OID 26001)
-- Name: ocp_procedure ocp_measrument_to_measurment_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ocp_procedure
    ADD CONSTRAINT ocp_measrument_to_measurment_id FOREIGN KEY (ocp_measurment_id) REFERENCES public.measurements(measurement_id) NOT VALID;


--
-- TOC entry 4816 (class 2606 OID 26006)
-- Name: ocp_raw ocp_raw_to_ocp_procedure; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ocp_raw
    ADD CONSTRAINT ocp_raw_to_ocp_procedure FOREIGN KEY (procedure_id) REFERENCES public.ocp_procedure(procedure_id) NOT VALID;


--
-- TOC entry 4812 (class 2606 OID 26011)
-- Name: experiments user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.experiments
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) NOT VALID;


--
-- TOC entry 4818 (class 2606 OID 26032)
-- Name: xps_c1s_raw xps_c1s_raw_to_xps_procedure; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.xps_c1s_raw
    ADD CONSTRAINT xps_c1s_raw_to_xps_procedure FOREIGN KEY (procedure_id) REFERENCES public.xps_procedure(procedure_id);


--
-- TOC entry 4819 (class 2606 OID 26042)
-- Name: xps_f1s_raw xps_f1s_raw_to_xps_procedure; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.xps_f1s_raw
    ADD CONSTRAINT xps_f1s_raw_to_xps_procedure FOREIGN KEY (procedure_id) REFERENCES public.xps_procedure(procedure_id);


--
-- TOC entry 4820 (class 2606 OID 26052)
-- Name: xps_li1s_raw xps_li1s_raw_to_xps_procedure; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.xps_li1s_raw
    ADD CONSTRAINT xps_li1s_raw_to_xps_procedure FOREIGN KEY (procedure_id) REFERENCES public.xps_procedure(procedure_id);


--
-- TOC entry 4817 (class 2606 OID 26022)
-- Name: xps_procedure xps_measrument_to_measurment_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.xps_procedure
    ADD CONSTRAINT xps_measrument_to_measurment_id FOREIGN KEY (xps_measurement_id) REFERENCES public.measurements(measurement_id) NOT VALID;


--
-- TOC entry 4821 (class 2606 OID 26067)
-- Name: xps_o1s_raw xps_o1s_raw_to_xps_procedure; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.xps_o1s_raw
    ADD CONSTRAINT xps_o1s_raw_to_xps_procedure FOREIGN KEY (procedure_id) REFERENCES public.xps_procedure(procedure_id);


-- Completed on 2023-12-31 00:29:38

--
-- PostgreSQL database dump complete
--

