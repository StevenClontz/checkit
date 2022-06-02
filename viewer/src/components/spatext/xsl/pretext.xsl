<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:stx="https://spatext.clontz.org"
                exclude-result-prefixes="stx">

    <xsl:output method="xml" indent="yes"/>

    <!-- kill undefined elements -->
    <xsl:template match="*"/>

    <!-- Normalize text() whitespace but don't completely trim beginning or end: https://stackoverflow.com/a/5044657/1607849 -->
    <xsl:template match="text()"><xsl:value-of select="translate(normalize-space(concat('&#x7F;',.,'&#x7F;')),'&#x7F;','')"/></xsl:template>

    <xsl:template match="/">
        <pretext>
            <xsl:apply-templates/>
        </pretext>
    </xsl:template>

    <xsl:template match="stx:knowl">
        <xsl:choose>
            <xsl:when test="ancestor::stx:knowl">
                <xsl:call-template name="knowl-content"/>
            </xsl:when>
            <xsl:when test="@mode='exercise'">
                <exercise><xsl:call-template name="knowl-content"/></exercise>
            </xsl:when>
            <xsl:otherwise>
                <theorem><xsl:call-template name="knowl-content"/></theorem>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template name="knowl-content">
        <xsl:apply-templates select="stx:title[1]"/>
        <xsl:apply-templates select="stx:intro[1]"/>
        <xsl:choose>
            <xsl:when test="stx:knowl">
                <task>
                    <xsl:for-each select="stx:knowl">
                        <task><xsl:call-template name="knowl-content"/></task>
                    </xsl:for-each>
                </task>
            </xsl:when>
            <xsl:otherwise>
                <statement>
                    <xsl:apply-templates select="stx:content[1]"/>
                </statement>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select="stx:outtro[1]"/>
    </xsl:template>

    <xsl:template match="stx:title">
        <title>
            <xsl:apply-templates select="text()|stx:m|stx:q|stx:c"/>
        </title>
    </xsl:template>

    <xsl:template match="stx:intro">
        <introduction>
            <xsl:apply-templates select="stx:p|stx:list"/>
        </introduction>
    </xsl:template>

    <xsl:template match="stx:content">
        <xsl:choose>
            <xsl:when test="ancestor::stx:knowl">
                <xsl:apply-templates select="stx:p|stx:list"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="stx:p|stx:list|stx:knowl"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="stx:outtro">
        <xsl:choose>
            <xsl:when test="ancestor::stx:knowl[@mode='exercise']">
                <answer>
                    <xsl:apply-templates select="stx:p|stx:list"/>
                </answer>
            </xsl:when>
            <xsl:otherwise>
                <conclusion>
                    <xsl:apply-templates select="stx:p|stx:list"/>
                </conclusion>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="stx:list">
        <xsl:if test="stx:item">
            <ul>
                <xsl:for-each select="stx:item">
                    <li>
                        <xsl:apply-templates select="stx:p|stx:list"/>
                    </li>
                </xsl:for-each>
            </ul>
        </xsl:if>
    </xsl:template>

    <xsl:template name="parseDisplay">
        <xsl:apply-templates select="text()|stx:m|stx:me|stx:q|stx:c|stx:em|stx:url|stx:image"/>
    </xsl:template>

    <xsl:template match="stx:p">
        <p>
            <xsl:call-template name="parseDisplay"/>
        </p>
    </xsl:template>

    <xsl:template match="stx:m">
        <m>
            <xsl:value-of select="normalize-space(text())"/>
        </m>
    </xsl:template>
    <xsl:template match="stx:m[@mode='display']|stx:me">
        <me>
            <xsl:value-of select="normalize-space(text())"/>
        </me>
    </xsl:template>

    <xsl:template match="stx:em">
        <em>
            <xsl:call-template name="parseDisplay"/>
        </em>
    </xsl:template>

    <xsl:template match="stx:c">
        <c>
            <xsl:value-of select="normalize-space(text())"/>
        </c>
    </xsl:template>

    <xsl:template match="stx:q">
        <q>
            <xsl:value-of select="normalize-space(text())"/>
        </q>
    </xsl:template>

    <xsl:template match="stx:image">
        <image>
            <xsl:attribute name="source">
                <xsl:value-of select="@source"/>
            </xsl:attribute>
            <xsl:attribute name="description">
                <xsl:value-of select="@description"/>
            </xsl:attribute>
        </image>
    </xsl:template>

    <xsl:template match="stx:url[@href]">
        <url>
            <xsl:attribute name="href">
                <xsl:value-of select="@href"/>
            </xsl:attribute>
            <xsl:call-template name="parseDisplay"/>
        </url>
    </xsl:template>

</xsl:stylesheet>