<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html"/>

    <!-- Normalize whitespace but don't completely trim beginning or end: https://stackoverflow.com/a/5044657/1607849 -->
    <xsl:template match="text()"><xsl:value-of select="translate(normalize-space(concat('&#x7F;',.,'&#x7F;')),'&#x7F;','')"/></xsl:template>

    <xsl:template match="exercise">
        <div class="checkit exercise">
            <xsl:attribute name="data-checkit-slug"><xsl:value-of select="@checkit-slug"/></xsl:attribute>
            <xsl:attribute name="data-checkit-title"><xsl:value-of select="@checkit-title"/></xsl:attribute>
            <xsl:attribute name="data-checkit-seed"><xsl:value-of select="@checkit-seed"/></xsl:attribute>
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="statement">
        <div class="exercise-statement"><xsl:apply-templates/></div>
    </xsl:template>

    <xsl:template match="answer">
        <div class="exercise-answer">
            <p><b>Answer:</b></p>
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="p">
        <p><xsl:apply-templates/></p>
    </xsl:template>

    <xsl:template match="claim">
        <p><xsl:apply-templates/></p>
    </xsl:template>

    <xsl:template match="me"><p class="math math-display">\[<xsl:value-of select="."/>\]</p></xsl:template>

        <xsl:template match="md">
        <xsl:choose>
            <xsl:when test="@alignment='alignat'">
                <p class="math math-display">\begin{alignat*}{<xsl:value-of select="normalize-space(@alignat-columns)"/>} <xsl:apply-templates select="mrow"/> \end{alignat*}</p>
            </xsl:when>
            <xsl:otherwise>
                <p class="math math-display">\begin{align*} <xsl:apply-templates select="mrow"/> \end{align*}</p>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="mrow"><xsl:value-of select="."/> \\</xsl:template>

    <xsl:template match="m"><span class="math math-inline">\(<xsl:value-of select="."/>\)</span></xsl:template>


    <xsl:template match="ul"><ul><xsl:apply-templates select="li"/></ul></xsl:template>
    <xsl:template match="ol"><ol type="a"><xsl:apply-templates select="li"/></ol></xsl:template>
    <xsl:template match="li"><li><xsl:apply-templates/></li></xsl:template>

    <xsl:template match="c"><code><xsl:value-of select="."/></code></xsl:template>
    <xsl:template match="url"><a><xsl:attribute name="href"><xsl:value-of select="@href"/></xsl:attribute><xsl:value-of select="@href"/></a></xsl:template>

    <xsl:template match="image"><img><xsl:attribute name="src"><xsl:value-of select="@source"/></xsl:attribute></img></xsl:template>

</xsl:stylesheet>