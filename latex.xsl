<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text"/>

    <xsl:template match="statement">

        <xsl:apply-templates/>

    </xsl:template>

    <xsl:template match="answer">

        \textbf{Answer:} <xsl:apply-templates/>

    </xsl:template>

    <xsl:template match="p">

        <xsl:apply-templates/>

    </xsl:template>

    <xsl:template match="me">\[<xsl:value-of select="."/>\]</xsl:template>

    <xsl:template match="m">\(<xsl:value-of select="."/>\)</xsl:template>

</xsl:stylesheet>