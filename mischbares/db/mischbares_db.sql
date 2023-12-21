PGDMP  5                    {            mischbares_test    16.1    16.0 {    D           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            E           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            F           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            G           1262    16565    mischbares_test    DATABASE     �   CREATE DATABASE mischbares_test WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
    DROP DATABASE mischbares_test;
                postgres    false            �            1259    16566    ca_procedure    TABLE     ~  CREATE TABLE public.ca_procedure (
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
     DROP TABLE public.ca_procedure;
       public         heap    postgres    false            �            1259    16569 !   ca_procedure_ca_measurment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ca_procedure_ca_measurment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.ca_procedure_ca_measurment_id_seq;
       public          postgres    false    215            H           0    0 !   ca_procedure_ca_measurment_id_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.ca_procedure_ca_measurment_id_seq OWNED BY public.ca_procedure.ca_measurment_id;
          public          postgres    false    216            �            1259    16570    ca_procedure_procedure_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ca_procedure_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.ca_procedure_procedure_id_seq;
       public          postgres    false    215            I           0    0    ca_procedure_procedure_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.ca_procedure_procedure_id_seq OWNED BY public.ca_procedure.procedure_id;
          public          postgres    false    217            �            1259    16571    ca_raw    TABLE     �  CREATE TABLE public.ca_raw (
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
    DROP TABLE public.ca_raw;
       public         heap    postgres    false            �            1259    16574    ca_raw_procedure_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ca_raw_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.ca_raw_procedure_id_seq;
       public          postgres    false    218            J           0    0    ca_raw_procedure_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.ca_raw_procedure_id_seq OWNED BY public.ca_raw.procedure_id;
          public          postgres    false    219            �            1259    16575    ca_raw_raw_id_seq    SEQUENCE     z   CREATE SEQUENCE public.ca_raw_raw_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.ca_raw_raw_id_seq;
       public          postgres    false    218            K           0    0    ca_raw_raw_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.ca_raw_raw_id_seq OWNED BY public.ca_raw.raw_id;
          public          postgres    false    220            �            1259    16576    cp_procedure    TABLE     I  CREATE TABLE public.cp_procedure (
    duration integer NOT NULL,
    applied_current double precision NOT NULL,
    interval_time double precision NOT NULL,
    initial_transition_time double precision,
    procedure_id bigint NOT NULL,
    cp_measurment_id bigint NOT NULL,
    initial_transition_potential double precision
);
     DROP TABLE public.cp_procedure;
       public         heap    postgres    false            �            1259    16579 !   cp_procedure_cp_measurment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cp_procedure_cp_measurment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.cp_procedure_cp_measurment_id_seq;
       public          postgres    false    221            L           0    0 !   cp_procedure_cp_measurment_id_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.cp_procedure_cp_measurment_id_seq OWNED BY public.cp_procedure.cp_measurment_id;
          public          postgres    false    222            �            1259    16580    cp_procedure_procedure_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cp_procedure_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.cp_procedure_procedure_id_seq;
       public          postgres    false    221            M           0    0    cp_procedure_procedure_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.cp_procedure_procedure_id_seq OWNED BY public.cp_procedure.procedure_id;
          public          postgres    false    223            �            1259    16581    cp_raw    TABLE     �  CREATE TABLE public.cp_raw (
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
    DROP TABLE public.cp_raw;
       public         heap    postgres    false            �            1259    16584    cp_raw_procedure_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cp_raw_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.cp_raw_procedure_id_seq;
       public          postgres    false    224            N           0    0    cp_raw_procedure_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.cp_raw_procedure_id_seq OWNED BY public.cp_raw.procedure_id;
          public          postgres    false    225            �            1259    16585    cp_raw_raw_id_seq    SEQUENCE     z   CREATE SEQUENCE public.cp_raw_raw_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.cp_raw_raw_id_seq;
       public          postgres    false    224            O           0    0    cp_raw_raw_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.cp_raw_raw_id_seq OWNED BY public.cp_raw.raw_id;
          public          postgres    false    226                        1259    16756    cv_cycle    TABLE     �  CREATE TABLE public.cv_cycle (
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
    DROP TABLE public.cv_cycle;
       public         heap    postgres    false                       1259    16764    cv_cycle_cycle_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cv_cycle_cycle_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.cv_cycle_cycle_id_seq;
       public          postgres    false    256            P           0    0    cv_cycle_cycle_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.cv_cycle_cycle_id_seq OWNED BY public.cv_cycle.cycle_id;
          public          postgres    false    257            �            1259    16755    cv_cycle_procedure_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cv_cycle_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.cv_cycle_procedure_id_seq;
       public          postgres    false    256            Q           0    0    cv_cycle_procedure_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.cv_cycle_procedure_id_seq OWNED BY public.cv_cycle.procedure_id;
          public          postgres    false    255            �            1259    16586 +   cv_staircase_procedure_cv_measurment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cv_staircase_procedure_cv_measurment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 B   DROP SEQUENCE public.cv_staircase_procedure_cv_measurment_id_seq;
       public          postgres    false            �            1259    16587 '   cv_staircase_procedure_procedure_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cv_staircase_procedure_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 >   DROP SEQUENCE public.cv_staircase_procedure_procedure_id_seq;
       public          postgres    false            �            1259    16588    cv_staircase_procedure    TABLE     K  CREATE TABLE public.cv_staircase_procedure (
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
 *   DROP TABLE public.cv_staircase_procedure;
       public         heap    postgres    false    228    227            �            1259    16593 !   cv_staircase_raw_procedure_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cv_staircase_raw_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.cv_staircase_raw_procedure_id_seq;
       public          postgres    false            �            1259    16594    cv_staircase_raw_raw_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cv_staircase_raw_raw_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.cv_staircase_raw_raw_id_seq;
       public          postgres    false            �            1259    16595    cv_staircase_raw    TABLE       CREATE TABLE public.cv_staircase_raw (
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
 $   DROP TABLE public.cv_staircase_raw;
       public         heap    postgres    false    230    231            �            1259    16600    eis_procedure    TABLE     :  CREATE TABLE public.eis_procedure (
    potential double precision NOT NULL,
    lower_freuqency double precision NOT NULL,
    upper_frequency double precision NOT NULL,
    potential_dc double precision,
    current_dc double precision,
    procedure_id bigint NOT NULL,
    eis_measurment_id bigint NOT NULL
);
 !   DROP TABLE public.eis_procedure;
       public         heap    postgres    false            �            1259    16603 #   eis_procedure_eis_measurment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.eis_procedure_eis_measurment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 :   DROP SEQUENCE public.eis_procedure_eis_measurment_id_seq;
       public          postgres    false    233            R           0    0 #   eis_procedure_eis_measurment_id_seq    SEQUENCE OWNED BY     k   ALTER SEQUENCE public.eis_procedure_eis_measurment_id_seq OWNED BY public.eis_procedure.eis_measurment_id;
          public          postgres    false    234            �            1259    16604    eis_procedure_procedure_id_seq    SEQUENCE     �   CREATE SEQUENCE public.eis_procedure_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.eis_procedure_procedure_id_seq;
       public          postgres    false    233            S           0    0    eis_procedure_procedure_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.eis_procedure_procedure_id_seq OWNED BY public.eis_procedure.procedure_id;
          public          postgres    false    235            �            1259    16605    eis_raw    TABLE     5  CREATE TABLE public.eis_raw (
    frequency double precision NOT NULL,
    z_real double precision NOT NULL,
    neg_z_imag double precision NOT NULL,
    z_norm double precision NOT NULL,
    neg_phase_shift double precision,
    procedure_id bigint NOT NULL,
    raw_id bigint NOT NULL,
    index bigint
);
    DROP TABLE public.eis_raw;
       public         heap    postgres    false            �            1259    16608    eis_raw_procedure_id_seq    SEQUENCE     �   CREATE SEQUENCE public.eis_raw_procedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.eis_raw_procedure_id_seq;
       public          postgres    false    236            T           0    0    eis_raw_procedure_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.eis_raw_procedure_id_seq OWNED BY public.eis_raw.procedure_id;
          public          postgres    false    237            �            1259    16609    eis_raw_raw_id_seq    SEQUENCE     {   CREATE SEQUENCE public.eis_raw_raw_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.eis_raw_raw_id_seq;
       public          postgres    false    236            U           0    0    eis_raw_raw_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.eis_raw_raw_id_seq OWNED BY public.eis_raw.raw_id;
          public          postgres    false    238            �            1259    16610    experiments    TABLE     �  CREATE TABLE public.experiments (
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
    DROP TABLE public.experiments;
       public         heap    postgres    false            �            1259    16613    experiment_experiment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.experiment_experiment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.experiment_experiment_id_seq;
       public          postgres    false    239            V           0    0    experiment_experiment_id_seq    SEQUENCE OWNED BY     ^   ALTER SEQUENCE public.experiment_experiment_id_seq OWNED BY public.experiments.experiment_id;
          public          postgres    false    240            �            1259    16614    experiment_user_seq    SEQUENCE     �   CREATE SEQUENCE public.experiment_user_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.experiment_user_seq;
       public          postgres    false    239            W           0    0    experiment_user_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.experiment_user_seq OWNED BY public.experiments.user_id;
          public          postgres    false    241            �            1259    16615    measurements    TABLE     �   CREATE TABLE public.measurements (
    measurement_id bigint NOT NULL,
    procedure_name character varying(20) NOT NULL,
    experiment_id bigint NOT NULL
);
     DROP TABLE public.measurements;
       public         heap    postgres    false            �            1259    16618    measurment_experiment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.measurment_experiment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.measurment_experiment_id_seq;
       public          postgres    false    242            X           0    0    measurment_experiment_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.measurment_experiment_id_seq OWNED BY public.measurements.experiment_id;
          public          postgres    false    243            �            1259    16619    measurment_measurment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.measurment_measurment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.measurment_measurment_id_seq;
       public          postgres    false    242            Y           0    0    measurment_measurment_id_seq    SEQUENCE OWNED BY     `   ALTER SEQUENCE public.measurment_measurment_id_seq OWNED BY public.measurements.measurement_id;
          public          postgres    false    244            �            1259    16620    motor_positions    TABLE     �   CREATE TABLE public.motor_positions (
    x_coordinate double precision,
    y_coordinate double precision,
    experiment_id integer NOT NULL,
    z_coordinate double precision
);
 #   DROP TABLE public.motor_positions;
       public         heap    postgres    false            �            1259    16623    motor_experiment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.motor_experiment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.motor_experiment_id_seq;
       public          postgres    false    245            Z           0    0    motor_experiment_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.motor_experiment_id_seq OWNED BY public.motor_positions.experiment_id;
          public          postgres    false    246            �            1259    16624    ocp_procedure    TABLE     �   CREATE TABLE public.ocp_procedure (
    duration integer,
    interval_time double precision,
    procedure_id integer NOT NULL,
    ocp_measurment_id bigint NOT NULL
);
 !   DROP TABLE public.ocp_procedure;
       public         heap    postgres    false            �            1259    16627 #   ocp_procedure_ocp_measurment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ocp_procedure_ocp_measurment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 :   DROP SEQUENCE public.ocp_procedure_ocp_measurment_id_seq;
       public          postgres    false    247            [           0    0 #   ocp_procedure_ocp_measurment_id_seq    SEQUENCE OWNED BY     k   ALTER SEQUENCE public.ocp_procedure_ocp_measurment_id_seq OWNED BY public.ocp_procedure.ocp_measurment_id;
          public          postgres    false    248            �            1259    16628    ocp_procedure_procedure_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ocp_procedure_procedure_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.ocp_procedure_procedure_id_seq;
       public          postgres    false    247            \           0    0    ocp_procedure_procedure_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.ocp_procedure_procedure_id_seq OWNED BY public.ocp_procedure.procedure_id;
          public          postgres    false    249            �            1259    16629    ocp_raw    TABLE     |  CREATE TABLE public.ocp_raw (
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
    DROP TABLE public.ocp_raw;
       public         heap    postgres    false            �            1259    16632    ocp_raw_ocp_procedure_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ocp_raw_ocp_procedure_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.ocp_raw_ocp_procedure_id_seq;
       public          postgres    false    250            ]           0    0    ocp_raw_ocp_procedure_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.ocp_raw_ocp_procedure_id_seq OWNED BY public.ocp_raw.procedure_id;
          public          postgres    false    251            �            1259    16633    ocp_raw_raw_id_seq    SEQUENCE     {   CREATE SEQUENCE public.ocp_raw_raw_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.ocp_raw_raw_id_seq;
       public          postgres    false    250            ^           0    0    ocp_raw_raw_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.ocp_raw_raw_id_seq OWNED BY public.ocp_raw.raw_id;
          public          postgres    false    252            �            1259    16634    users    TABLE       CREATE TABLE public.users (
    user_id integer NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(50) NOT NULL,
    password character varying,
    username character varying
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    16639    user_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.user_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.user_user_id_seq;
       public          postgres    false    253            _           0    0    user_user_id_seq    SEQUENCE OWNED BY     F   ALTER SEQUENCE public.user_user_id_seq OWNED BY public.users.user_id;
          public          postgres    false    254            m           2604    16640    ca_procedure procedure_id    DEFAULT     �   ALTER TABLE ONLY public.ca_procedure ALTER COLUMN procedure_id SET DEFAULT nextval('public.ca_procedure_procedure_id_seq'::regclass);
 H   ALTER TABLE public.ca_procedure ALTER COLUMN procedure_id DROP DEFAULT;
       public          postgres    false    217    215            n           2604    16641    ca_procedure ca_measurment_id    DEFAULT     �   ALTER TABLE ONLY public.ca_procedure ALTER COLUMN ca_measurment_id SET DEFAULT nextval('public.ca_procedure_ca_measurment_id_seq'::regclass);
 L   ALTER TABLE public.ca_procedure ALTER COLUMN ca_measurment_id DROP DEFAULT;
       public          postgres    false    216    215            o           2604    16642    ca_raw procedure_id    DEFAULT     z   ALTER TABLE ONLY public.ca_raw ALTER COLUMN procedure_id SET DEFAULT nextval('public.ca_raw_procedure_id_seq'::regclass);
 B   ALTER TABLE public.ca_raw ALTER COLUMN procedure_id DROP DEFAULT;
       public          postgres    false    219    218            p           2604    16643    ca_raw raw_id    DEFAULT     n   ALTER TABLE ONLY public.ca_raw ALTER COLUMN raw_id SET DEFAULT nextval('public.ca_raw_raw_id_seq'::regclass);
 <   ALTER TABLE public.ca_raw ALTER COLUMN raw_id DROP DEFAULT;
       public          postgres    false    220    218            q           2604    16644    cp_procedure procedure_id    DEFAULT     �   ALTER TABLE ONLY public.cp_procedure ALTER COLUMN procedure_id SET DEFAULT nextval('public.cp_procedure_procedure_id_seq'::regclass);
 H   ALTER TABLE public.cp_procedure ALTER COLUMN procedure_id DROP DEFAULT;
       public          postgres    false    223    221            r           2604    16645    cp_procedure cp_measurment_id    DEFAULT     �   ALTER TABLE ONLY public.cp_procedure ALTER COLUMN cp_measurment_id SET DEFAULT nextval('public.cp_procedure_cp_measurment_id_seq'::regclass);
 L   ALTER TABLE public.cp_procedure ALTER COLUMN cp_measurment_id DROP DEFAULT;
       public          postgres    false    222    221            s           2604    16646    cp_raw procedure_id    DEFAULT     z   ALTER TABLE ONLY public.cp_raw ALTER COLUMN procedure_id SET DEFAULT nextval('public.cp_raw_procedure_id_seq'::regclass);
 B   ALTER TABLE public.cp_raw ALTER COLUMN procedure_id DROP DEFAULT;
       public          postgres    false    225    224            t           2604    16647    cp_raw raw_id    DEFAULT     n   ALTER TABLE ONLY public.cp_raw ALTER COLUMN raw_id SET DEFAULT nextval('public.cp_raw_raw_id_seq'::regclass);
 <   ALTER TABLE public.cp_raw ALTER COLUMN raw_id DROP DEFAULT;
       public          postgres    false    226    224            �           2604    16759    cv_cycle procedure_id    DEFAULT     ~   ALTER TABLE ONLY public.cv_cycle ALTER COLUMN procedure_id SET DEFAULT nextval('public.cv_cycle_procedure_id_seq'::regclass);
 D   ALTER TABLE public.cv_cycle ALTER COLUMN procedure_id DROP DEFAULT;
       public          postgres    false    255    256    256            �           2604    16765    cv_cycle cycle_id    DEFAULT     v   ALTER TABLE ONLY public.cv_cycle ALTER COLUMN cycle_id SET DEFAULT nextval('public.cv_cycle_cycle_id_seq'::regclass);
 @   ALTER TABLE public.cv_cycle ALTER COLUMN cycle_id DROP DEFAULT;
       public          postgres    false    257    256            y           2604    16648    eis_procedure procedure_id    DEFAULT     �   ALTER TABLE ONLY public.eis_procedure ALTER COLUMN procedure_id SET DEFAULT nextval('public.eis_procedure_procedure_id_seq'::regclass);
 I   ALTER TABLE public.eis_procedure ALTER COLUMN procedure_id DROP DEFAULT;
       public          postgres    false    235    233            z           2604    16649    eis_procedure eis_measurment_id    DEFAULT     �   ALTER TABLE ONLY public.eis_procedure ALTER COLUMN eis_measurment_id SET DEFAULT nextval('public.eis_procedure_eis_measurment_id_seq'::regclass);
 N   ALTER TABLE public.eis_procedure ALTER COLUMN eis_measurment_id DROP DEFAULT;
       public          postgres    false    234    233            {           2604    16650    eis_raw procedure_id    DEFAULT     |   ALTER TABLE ONLY public.eis_raw ALTER COLUMN procedure_id SET DEFAULT nextval('public.eis_raw_procedure_id_seq'::regclass);
 C   ALTER TABLE public.eis_raw ALTER COLUMN procedure_id DROP DEFAULT;
       public          postgres    false    237    236            |           2604    16651    eis_raw raw_id    DEFAULT     p   ALTER TABLE ONLY public.eis_raw ALTER COLUMN raw_id SET DEFAULT nextval('public.eis_raw_raw_id_seq'::regclass);
 =   ALTER TABLE public.eis_raw ALTER COLUMN raw_id DROP DEFAULT;
       public          postgres    false    238    236            }           2604    16652    experiments experiment_id    DEFAULT     �   ALTER TABLE ONLY public.experiments ALTER COLUMN experiment_id SET DEFAULT nextval('public.experiment_experiment_id_seq'::regclass);
 H   ALTER TABLE public.experiments ALTER COLUMN experiment_id DROP DEFAULT;
       public          postgres    false    240    239            ~           2604    16653    experiments user_id    DEFAULT     v   ALTER TABLE ONLY public.experiments ALTER COLUMN user_id SET DEFAULT nextval('public.experiment_user_seq'::regclass);
 B   ALTER TABLE public.experiments ALTER COLUMN user_id DROP DEFAULT;
       public          postgres    false    241    239                       2604    16654    measurements measurement_id    DEFAULT     �   ALTER TABLE ONLY public.measurements ALTER COLUMN measurement_id SET DEFAULT nextval('public.measurment_measurment_id_seq'::regclass);
 J   ALTER TABLE public.measurements ALTER COLUMN measurement_id DROP DEFAULT;
       public          postgres    false    244    242            �           2604    16655    measurements experiment_id    DEFAULT     �   ALTER TABLE ONLY public.measurements ALTER COLUMN experiment_id SET DEFAULT nextval('public.measurment_experiment_id_seq'::regclass);
 I   ALTER TABLE public.measurements ALTER COLUMN experiment_id DROP DEFAULT;
       public          postgres    false    243    242            �           2604    16656    motor_positions experiment_id    DEFAULT     �   ALTER TABLE ONLY public.motor_positions ALTER COLUMN experiment_id SET DEFAULT nextval('public.motor_experiment_id_seq'::regclass);
 L   ALTER TABLE public.motor_positions ALTER COLUMN experiment_id DROP DEFAULT;
       public          postgres    false    246    245            �           2604    16657    ocp_procedure procedure_id    DEFAULT     �   ALTER TABLE ONLY public.ocp_procedure ALTER COLUMN procedure_id SET DEFAULT nextval('public.ocp_procedure_procedure_id_seq'::regclass);
 I   ALTER TABLE public.ocp_procedure ALTER COLUMN procedure_id DROP DEFAULT;
       public          postgres    false    249    247            �           2604    16658    ocp_procedure ocp_measurment_id    DEFAULT     �   ALTER TABLE ONLY public.ocp_procedure ALTER COLUMN ocp_measurment_id SET DEFAULT nextval('public.ocp_procedure_ocp_measurment_id_seq'::regclass);
 N   ALTER TABLE public.ocp_procedure ALTER COLUMN ocp_measurment_id DROP DEFAULT;
       public          postgres    false    248    247            �           2604    16659    ocp_raw procedure_id    DEFAULT     �   ALTER TABLE ONLY public.ocp_raw ALTER COLUMN procedure_id SET DEFAULT nextval('public.ocp_raw_ocp_procedure_id_seq'::regclass);
 C   ALTER TABLE public.ocp_raw ALTER COLUMN procedure_id DROP DEFAULT;
       public          postgres    false    251    250            �           2604    16660    ocp_raw raw_id    DEFAULT     p   ALTER TABLE ONLY public.ocp_raw ALTER COLUMN raw_id SET DEFAULT nextval('public.ocp_raw_raw_id_seq'::regclass);
 =   ALTER TABLE public.ocp_raw ALTER COLUMN raw_id DROP DEFAULT;
       public          postgres    false    252    250            �           2604    16661    users user_id    DEFAULT     m   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.user_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public          postgres    false    254    253            �           2606    16663    ca_procedure ca_procedure_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.ca_procedure
    ADD CONSTRAINT ca_procedure_pkey PRIMARY KEY (procedure_id);
 H   ALTER TABLE ONLY public.ca_procedure DROP CONSTRAINT ca_procedure_pkey;
       public            postgres    false    215            �           2606    16665    ca_raw ca_raw_to_id_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.ca_raw
    ADD CONSTRAINT ca_raw_to_id_pkey PRIMARY KEY (raw_id);
 B   ALTER TABLE ONLY public.ca_raw DROP CONSTRAINT ca_raw_to_id_pkey;
       public            postgres    false    218            �           2606    16667    cp_procedure cp_procedure_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.cp_procedure
    ADD CONSTRAINT cp_procedure_pkey PRIMARY KEY (procedure_id);
 H   ALTER TABLE ONLY public.cp_procedure DROP CONSTRAINT cp_procedure_pkey;
       public            postgres    false    221            �           2606    16669    cp_raw cp_raw_to_id_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.cp_raw
    ADD CONSTRAINT cp_raw_to_id_pkey PRIMARY KEY (raw_id);
 B   ALTER TABLE ONLY public.cp_raw DROP CONSTRAINT cp_raw_to_id_pkey;
       public            postgres    false    224            �           2606    16772    cv_cycle cv_cycle_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.cv_cycle
    ADD CONSTRAINT cv_cycle_pkey PRIMARY KEY (cycle_id);
 @   ALTER TABLE ONLY public.cv_cycle DROP CONSTRAINT cv_cycle_pkey;
       public            postgres    false    256            �           2606    16671 (   cv_staircase_procedure cv_procedure_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.cv_staircase_procedure
    ADD CONSTRAINT cv_procedure_pkey PRIMARY KEY (procedure_id);
 R   ALTER TABLE ONLY public.cv_staircase_procedure DROP CONSTRAINT cv_procedure_pkey;
       public            postgres    false    229            �           2606    16673 "   cv_staircase_raw cv_raw_to_id_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.cv_staircase_raw
    ADD CONSTRAINT cv_raw_to_id_pkey PRIMARY KEY (raw_id);
 L   ALTER TABLE ONLY public.cv_staircase_raw DROP CONSTRAINT cv_raw_to_id_pkey;
       public            postgres    false    232            �           2606    16675     eis_procedure eis_procedure_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.eis_procedure
    ADD CONSTRAINT eis_procedure_pkey PRIMARY KEY (procedure_id);
 J   ALTER TABLE ONLY public.eis_procedure DROP CONSTRAINT eis_procedure_pkey;
       public            postgres    false    233            �           2606    16677    eis_raw eis_raw_to_id_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.eis_raw
    ADD CONSTRAINT eis_raw_to_id_pkey PRIMARY KEY (raw_id);
 D   ALTER TABLE ONLY public.eis_raw DROP CONSTRAINT eis_raw_to_id_pkey;
       public            postgres    false    236            �           2606    16679    experiments experiment_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.experiments
    ADD CONSTRAINT experiment_pkey PRIMARY KEY (experiment_id);
 E   ALTER TABLE ONLY public.experiments DROP CONSTRAINT experiment_pkey;
       public            postgres    false    239            �           2606    16681    measurements measurment_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.measurements
    ADD CONSTRAINT measurment_pkey PRIMARY KEY (measurement_id);
 F   ALTER TABLE ONLY public.measurements DROP CONSTRAINT measurment_pkey;
       public            postgres    false    242            �           2606    16683     ocp_procedure ocp_procedure_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.ocp_procedure
    ADD CONSTRAINT ocp_procedure_pkey PRIMARY KEY (procedure_id);
 J   ALTER TABLE ONLY public.ocp_procedure DROP CONSTRAINT ocp_procedure_pkey;
       public            postgres    false    247            �           2606    16685    ocp_raw ocp_raw_id_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.ocp_raw
    ADD CONSTRAINT ocp_raw_id_pkey PRIMARY KEY (raw_id);
 A   ALTER TABLE ONLY public.ocp_raw DROP CONSTRAINT ocp_raw_id_pkey;
       public            postgres    false    250            �           2606    16687    users user_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.users
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);
 9   ALTER TABLE ONLY public.users DROP CONSTRAINT user_pkey;
       public            postgres    false    253            �           2606    16688 +   ca_procedure ca_measrument_to_measurment_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.ca_procedure
    ADD CONSTRAINT ca_measrument_to_measurment_id FOREIGN KEY (ca_measurment_id) REFERENCES public.measurements(measurement_id) NOT VALID;
 U   ALTER TABLE ONLY public.ca_procedure DROP CONSTRAINT ca_measrument_to_measurment_id;
       public          postgres    false    242    4764    215            �           2606    16693    ca_raw ca_raw_to_ca_procedure    FK CONSTRAINT     �   ALTER TABLE ONLY public.ca_raw
    ADD CONSTRAINT ca_raw_to_ca_procedure FOREIGN KEY (procedure_id) REFERENCES public.ca_procedure(procedure_id) NOT VALID;
 G   ALTER TABLE ONLY public.ca_raw DROP CONSTRAINT ca_raw_to_ca_procedure;
       public          postgres    false    4746    218    215            �           2606    16698 +   cp_procedure cp_measrument_to_measurment_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.cp_procedure
    ADD CONSTRAINT cp_measrument_to_measurment_id FOREIGN KEY (cp_measurment_id) REFERENCES public.measurements(measurement_id) NOT VALID;
 U   ALTER TABLE ONLY public.cp_procedure DROP CONSTRAINT cp_measrument_to_measurment_id;
       public          postgres    false    221    4764    242            �           2606    16703    cp_raw cp_raw_to_cp_procedure    FK CONSTRAINT     �   ALTER TABLE ONLY public.cp_raw
    ADD CONSTRAINT cp_raw_to_cp_procedure FOREIGN KEY (procedure_id) REFERENCES public.cp_procedure(procedure_id) NOT VALID;
 G   ALTER TABLE ONLY public.cp_raw DROP CONSTRAINT cp_raw_to_cp_procedure;
       public          postgres    false    224    4750    221            �           2606    16773 !   cv_cycle cv_cycle_to_cv_procedure    FK CONSTRAINT     �   ALTER TABLE ONLY public.cv_cycle
    ADD CONSTRAINT cv_cycle_to_cv_procedure FOREIGN KEY (procedure_id) REFERENCES public.cv_staircase_procedure(procedure_id) NOT VALID;
 K   ALTER TABLE ONLY public.cv_cycle DROP CONSTRAINT cv_cycle_to_cv_procedure;
       public          postgres    false    256    229    4754            �           2606    16708 5   cv_staircase_procedure cv_measrument_to_measurment_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.cv_staircase_procedure
    ADD CONSTRAINT cv_measrument_to_measurment_id FOREIGN KEY (cv_measurment_id) REFERENCES public.measurements(measurement_id) NOT VALID;
 _   ALTER TABLE ONLY public.cv_staircase_procedure DROP CONSTRAINT cv_measrument_to_measurment_id;
       public          postgres    false    229    242    4764            �           2606    16713 '   cv_staircase_raw cv_raw_to_cv_procedure    FK CONSTRAINT     �   ALTER TABLE ONLY public.cv_staircase_raw
    ADD CONSTRAINT cv_raw_to_cv_procedure FOREIGN KEY (procedure_id) REFERENCES public.cv_staircase_procedure(procedure_id) NOT VALID;
 Q   ALTER TABLE ONLY public.cv_staircase_raw DROP CONSTRAINT cv_raw_to_cv_procedure;
       public          postgres    false    229    232    4754            �           2606    16718 -   eis_procedure eis_measrument_to_measurment_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.eis_procedure
    ADD CONSTRAINT eis_measrument_to_measurment_id FOREIGN KEY (eis_measurment_id) REFERENCES public.measurements(measurement_id) NOT VALID;
 W   ALTER TABLE ONLY public.eis_procedure DROP CONSTRAINT eis_measrument_to_measurment_id;
       public          postgres    false    242    4764    233            �           2606    16723     eis_raw eis_raw_to_eis_procedure    FK CONSTRAINT     �   ALTER TABLE ONLY public.eis_raw
    ADD CONSTRAINT eis_raw_to_eis_procedure FOREIGN KEY (procedure_id) REFERENCES public.eis_procedure(procedure_id) NOT VALID;
 J   ALTER TABLE ONLY public.eis_raw DROP CONSTRAINT eis_raw_to_eis_procedure;
       public          postgres    false    4758    236    233            �           2606    16728    motor_positions experiment    FK CONSTRAINT     �   ALTER TABLE ONLY public.motor_positions
    ADD CONSTRAINT experiment FOREIGN KEY (experiment_id) REFERENCES public.experiments(experiment_id);
 D   ALTER TABLE ONLY public.motor_positions DROP CONSTRAINT experiment;
       public          postgres    false    4762    239    245            �           2606    16733 +   measurements measurment_id_to_experiment_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.measurements
    ADD CONSTRAINT measurment_id_to_experiment_id FOREIGN KEY (experiment_id) REFERENCES public.experiments(experiment_id);
 U   ALTER TABLE ONLY public.measurements DROP CONSTRAINT measurment_id_to_experiment_id;
       public          postgres    false    4762    239    242            �           2606    16738 -   ocp_procedure ocp_measrument_to_measurment_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.ocp_procedure
    ADD CONSTRAINT ocp_measrument_to_measurment_id FOREIGN KEY (ocp_measurment_id) REFERENCES public.measurements(measurement_id) NOT VALID;
 W   ALTER TABLE ONLY public.ocp_procedure DROP CONSTRAINT ocp_measrument_to_measurment_id;
       public          postgres    false    242    247    4764            �           2606    16743     ocp_raw ocp_raw_to_ocp_procedure    FK CONSTRAINT     �   ALTER TABLE ONLY public.ocp_raw
    ADD CONSTRAINT ocp_raw_to_ocp_procedure FOREIGN KEY (procedure_id) REFERENCES public.ocp_procedure(procedure_id) NOT VALID;
 J   ALTER TABLE ONLY public.ocp_raw DROP CONSTRAINT ocp_raw_to_ocp_procedure;
       public          postgres    false    4766    250    247            �           2606    16748    experiments user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.experiments
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) NOT VALID;
 =   ALTER TABLE ONLY public.experiments DROP CONSTRAINT user_id;
       public          postgres    false    239    4770    253           