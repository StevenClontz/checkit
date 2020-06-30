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

    <xsl:template match="m">\(<xsl:value-of select="."/>\)</xsl:template>

</xsl:stylesheet>