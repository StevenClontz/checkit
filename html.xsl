<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html"/>

    <xsl:template match="statement">
        <div><xsl:apply-templates/></div>
    </xsl:template>

    <xsl:template match="answer">
        <div>
            <p><b>Answer:</b></p>
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="p">
        <p><xsl:apply-templates/></p>
    </xsl:template>

    <xsl:template match="me"><p>\[<xsl:value-of select="."/>\]</p></xsl:template>

    <xsl:template match="md">\[\begin{align*}<xsl:apply-templates select="mrow"/>\end{align*}\]</xsl:template>

    <xsl:template match="mrow"><xsl:value-of select="."/> \\</xsl:template>

    <xsl:template match="m">\(<xsl:value-of select="."/>\)</xsl:template>

    <xsl:template match="ul"><ul><xsl:apply-templates select="li"/></ul></xsl:template>
    <xsl:template match="ol"><ol type="a"><xsl:apply-templates select="li"/></ol></xsl:template>
    <xsl:template match="li"><li><xsl:apply-templates/></li></xsl:template>


</xsl:stylesheet>