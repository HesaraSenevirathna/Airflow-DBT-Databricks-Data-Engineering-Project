{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%} {{ default_schema }}

    {%- else -%} {{ custom_schema_name | trim }}

    {%- endif -%}

{%- endmacro %}

# https://docs.getdbt.com/docs/build/custom-schemas?version=2.0&name=Fusion
