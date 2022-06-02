<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:stx="https://spatext.clontz.org"
                exclude-result-prefixes="stx">

    <xsl:output method="text"/>

    <!-- kill undefined elements -->
    <xsl:template match="*"/>

    <!-- Normalize text() whitespace but don't completely trim beginning or end: https://stackoverflow.com/a/5044657/1607849 -->
    <xsl:template match="text()"><xsl:value-of select="translate(normalize-space(concat('&#x7F;',.,'&#x7F;')),'&#x7F;','')"/></xsl:template>

    <xsl:template match="/">
        <xsl:text>%%%%% SpaTeXt Commands %%%%%</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:text>\providecommand{\stxKnowl}{}\renewcommand{\stxKnowl}[1]{#1}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:text>\providecommand{\stxOuttro}{}\renewcommand{\stxOuttro}[1]{#1}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:text>\providecommand{\stxTitle}{}\renewcommand{\stxTitle}[1]{#1}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:text>% Comment next line to show outtros</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:text>\renewcommand{\stxOuttro}[1]{}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:text>%%%%%%%%%%%%%%%%%%%%%%%%%%%%</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:apply-templates select="*"/>
    </xsl:template>

    <xsl:template match="stx:knowl">
        <xsl:text>\stxKnowl{</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:apply-templates select="stx:title[1]"/>
        <xsl:apply-templates select="stx:intro[1]"/>
        <xsl:choose>
            <xsl:when test="stx:knowl">
                <xsl:text>\begin{enumerate}</xsl:text>
                <xsl:text>&#xa;</xsl:text>
                <xsl:for-each select="stx:knowl">
                    <xsl:text>\item</xsl:text>
                    <xsl:text>&#xa;</xsl:text>
                    <xsl:apply-templates select="."/>
                </xsl:for-each>
                <xsl:text>\end{enumerate}</xsl:text>
                <xsl:text>&#xa;</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="stx:content[1]"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select="stx:outtro[1]"/>
        <xsl:text>}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>

    <xsl:template match="stx:title">
        <xsl:text>\stxTitle{</xsl:text>
        <xsl:apply-templates select="text()|stx:m|stx:q|stx:c"/>
        <xsl:text>}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>

    <xsl:template match="stx:intro">
        <xsl:apply-templates select="stx:p|stx:list"/>
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
        <xsl:text>\stxOuttro{</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:apply-templates select="stx:p|stx:list"/>
        <xsl:text>}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>

    <xsl:template match="stx:list">
        <xsl:if test="stx:item">
            <xsl:text>\begin{itemize}</xsl:text>
            <xsl:text>&#xa;</xsl:text>
                <xsl:for-each select="stx:item">
                    <xsl:text>\item</xsl:text>
                    <xsl:text>&#xa;</xsl:text>
                    <xsl:apply-templates select="stx:p|stx:list"/>
                </xsl:for-each>
            <xsl:text>\end{itemize}</xsl:text>
            <xsl:text>&#xa;</xsl:text>
        </xsl:if>
    </xsl:template>

    <xsl:template name="parseDisplay">
        <xsl:apply-templates select="text()|stx:m|stx:me|stx:q|stx:c|stx:em|stx:url|stx:image"/>
    </xsl:template>

    <xsl:template match="stx:p">
        <xsl:call-template name="parseDisplay"/>
        <xsl:text>&#xa;&#xa;</xsl:text>
    </xsl:template>

    <xsl:template match="stx:m">
        <xsl:text>\(</xsl:text>
        <xsl:value-of select="normalize-space(text())"/>
        <xsl:text>\)</xsl:text>
    </xsl:template>
    <xsl:template match="stx:m[@mode='display']|stx:me">
        <xsl:text>\[</xsl:text>
        <xsl:value-of select="normalize-space(text())"/>
        <xsl:text>\]</xsl:text>
    </xsl:template>

    <xsl:template match="stx:em">
        <xsl:text>\textbf{</xsl:text>
        <xsl:call-template name="parseDisplay"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="stx:c">
        <xsl:text>\texttt{</xsl:text>
        <xsl:value-of select="normalize-space(text())"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="stx:q">
        <xsl:text>``</xsl:text>
        <xsl:call-template name="parseDisplay"/>
        <xsl:text>''</xsl:text>
    </xsl:template>

    <xsl:template match="stx:image">
        <xsl:text>\includegraphics{</xsl:text>
        <xsl:value-of select="@source"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="stx:url[@href]">
        <xsl:choose>
            <xsl:when test=". != ''">
                <xsl:text>\href{</xsl:text>
                <xsl:value-of select="@href"/>
                <xsl:text>}{</xsl:text>
                <xsl:call-template name="parseDisplay"/>
                <xsl:text>}</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>\url{</xsl:text>
                <xsl:value-of select="@href"/>
                <xsl:text>}</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>