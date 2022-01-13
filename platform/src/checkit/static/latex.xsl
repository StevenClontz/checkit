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
        <xsl:apply-templates select="stx:exercise"/>
    </xsl:template>

    <xsl:template match="stx:exercise">
        <xsl:text>\begin{checkitExercise}{</xsl:text>
        <xsl:value-of select="@checkit-slug"/>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="@checkit-title"/>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="@checkit-seed"/>
        <xsl:text>}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:apply-templates select="stx:statement"/>
        <xsl:choose>
            <xsl:when test="stx:task">
                <xsl:text>\begin{checkitTaskStatements}</xsl:text>
                <xsl:text>&#xa;</xsl:text>
                <xsl:apply-templates select="stx:task" mode="statement"/>
                <xsl:text>&#xa;</xsl:text>
                <xsl:text>\end{checkitTaskStatements}</xsl:text>
                <xsl:text>&#xa;</xsl:text>
                <xsl:text>\begin{checkitTaskAnswers}</xsl:text>
                <xsl:text>&#xa;</xsl:text>
                <xsl:apply-templates select="stx:task" mode="answer"/>
                <xsl:text>&#xa;</xsl:text>
                <xsl:text>\end{checkitTaskAnswers}</xsl:text>
                <xsl:text>&#xa;</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="stx:answer"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="stx:task" mode="statement">
        <xsl:text>\begin{checkitTaskStatement}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:apply-templates select="stx:statement"/>
        <xsl:text>&#xa;</xsl:text>
        <xsl:text>\end{checkitTaskStatement}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:if test="stx:task">
            <xsl:text>\begin{checkitTaskStatements}</xsl:text>
            <xsl:text>&#xa;</xsl:text>
            <xsl:apply-templates select="stx:task" mode="statement"/>
            <xsl:text>&#xa;</xsl:text>
            <xsl:text>\end{checkitTaskStatements}</xsl:text>
            <xsl:text>&#xa;</xsl:text>
        </xsl:if>
    </xsl:template>

    <xsl:template match="stx:task" mode="answer">
        <xsl:choose>
            <xsl:when test="stx:task">
                <xsl:text>\begin{checkitTaskAnswers}</xsl:text>
                <xsl:text>&#xa;</xsl:text>
                <xsl:apply-templates select="stx:task" mode="answer"/>
                <xsl:text>&#xa;</xsl:text>
                <xsl:text>\end{checkitTaskAnswers}</xsl:text>
                <xsl:text>&#xa;</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>\begin{checkitTaskAnswer}</xsl:text>
                <xsl:text>&#xa;</xsl:text>
                <xsl:apply-templates select="stx:answer"/>
                <xsl:text>&#xa;</xsl:text>
                <xsl:text>\end{checkitTaskAnswer}</xsl:text>
                <xsl:text>&#xa;</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="stx:statement">
        <xsl:text>\begin{checkitStatement}{</xsl:text>
        <xsl:value-of select="stx:title"/>
        <xsl:text>}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:apply-templates select="stx:p|stx:ul"/>
        <xsl:text>\end{checkitStatement}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>

    <xsl:template match="stx:answer">
        <xsl:text>\begin{checkitAnswer}{</xsl:text>
        <xsl:choose>
            <xsl:when test="stx:title">
                <xsl:value-of select="stx:title"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>Brief Answer:</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:apply-templates select="stx:p|stx:ul"/>
        <xsl:text>\end{checkitAnswer}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>

    <xsl:template match="stx:p">
        <xsl:apply-templates select="text()|stx:m|stx:me|stx:q|stx:c|stx:em|stx:url"/>
        <xsl:text>&#xa;&#xa;</xsl:text>
    </xsl:template>

    <xsl:template match="stx:ul">
        <xsl:text>\begin{itemize}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:apply-templates select="stx:li"/>
        <xsl:text>\end{itemize}</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>
    <xsl:template match="stx:li">
        <xsl:text>\item </xsl:text>
        <xsl:if test="stx:title">
            <xsl:text>\textbf{</xsl:text>
            <xsl:value-of select="stx:title"/>
            <xsl:text>} </xsl:text>
        </xsl:if>
        <xsl:apply-templates select="stx:p|stx:ul"/>
    </xsl:template>

    <xsl:template match="stx:m">
        <xsl:text>\(</xsl:text>
        <xsl:value-of select="normalize-space(text())"/>
        <xsl:text>\)</xsl:text>
    </xsl:template>
    <xsl:template match="stx:m[@style='display']|stx:me">
        <xsl:text>\[</xsl:text>
        <xsl:value-of select="normalize-space(text())"/>
        <xsl:text>\]</xsl:text>
    </xsl:template>

    <xsl:template match="stx:em">
        <xsl:text>\textbf{</xsl:text>
        <xsl:apply-templates select="text()|stx:m|stx:me|stx:q|stx:c|stx:em|stx:url"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="stx:c">
        <xsl:text>\verb|</xsl:text>
        <xsl:value-of select="normalize-space(text())"/>
        <xsl:text>|</xsl:text>
    </xsl:template>

    <xsl:template match="stx:q">
        <xsl:text>``</xsl:text>
        <xsl:apply-templates select="text()|stx:m|stx:me|stx:q|stx:c|stx:em|stx:url"/>
        <xsl:text>''</xsl:text>
    </xsl:template>

    <xsl:template match="stx:url[@href]">
        <xsl:choose>
            <xsl:when test="text()">
                <xsl:text>\href{</xsl:text>
                <xsl:value-of select="@href"/>
                <xsl:text>}{</xsl:text>
                <xsl:value-of select="normalize-space(text())"/>
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